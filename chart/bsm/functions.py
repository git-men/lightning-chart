import logging

from django.apps import apps
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import TruncDay, TruncMonth, TruncHour
from django.db.models import Sum, Count, F, Avg, Max, Min

from api_basebone.restful.serializers import get_model_exclude_fields
from api_basebone.utils.operators import build_filter_conditions2
from api_basebone.services.expresstion import resolve_expression
from api_basebone.drf.response import success_response
from api_basebone.restful.funcs import bsm_func
from api_basebone.core import exceptions

from chart.models import Chart
from guardian.shortcuts import GroupObjectPermission, assign_perm
from guardian.models import UserObjectPermission

log = logging.getLogger(__name__)


def group_statistics_data(fields, group_kwargs, model, *args, **kwargs):
    """
    分组统计
    """
    methods = {
        'sum': Sum,
        'Sum': Sum,
        'count': Count,
        'Count': Count,
        'Avg': Avg,
        'Max': Max,
        'Min': Min,
        None: F,
    }
    log.debug(f'static parameters, fields: {fields}, groups: {group_kwargs}')
    queryset = (
        model.objects.all().annotate(**group_kwargs).values(*group_kwargs.keys())
    )
    result = queryset.annotate(
        **{
            key: methods[value.get('method', None)](
                value['field'].replace('.', '__'),
                **{'distinct': value['distinct']} if 'distinct' in value else {}
            )
            for key, value in fields.items()
            # 排除exclude_fields
            if 'field' in value and value['field'] not in get_model_exclude_fields(model, None)
        },
        **{
            key: resolve_expression(value['expression'])
            for key, value in fields.items()
            if 'expression' in value
        }
    ).order_by(*group_kwargs.keys())
    # 支持排序
    sort_keys = kwargs.get('sort_keys', [])
    top_max = kwargs.get('top_max', None)
    # SORT_ASCE = 'asce'
    # SORT_DESC = 'desc'
    # all_keys = list(fields.keys()) + list(group_kwargs.keys())
    if sort_keys:
        # import re
        #
        # keys_set = set([re.sub(r'-', "", key) for key in sort_keys])
        # if not (keys_set & set(all_keys) == keys_set):
        #     pass
        result = result.order_by(*sort_keys)
    # 支持对聚合后的数据进行filter
    filters = kwargs.get('filters', [])
    if filters:
        con = build_filter_conditions2(filters)
        result = result.filter(con)
    # 筛选前N条
    if top_max:
        result = result[:top_max]
    # TODO 考虑使用DRF来序列化查询结果

    return result


def get_group_data(group):
    group_functions = {
        'TruncDay': TruncDay,
        'TruncMonth': TruncMonth,
        'TruncHour': TruncHour,
        None: F,
    }

    # TODO 解决重名的方法，例如供应商名称传过来的是'agency.name'，那么SQL应该同时group by agency_id 和 agency__name，而不单单是agency__name
    # 支持一下使用计算字段作为
    data = {}
    for k, v in group.items():
        if v.get('expression', None):
            expression = resolve_expression(v['expression'])
            log.debug(
                f'expression before: {v["expression"]} after resolve: {expression}'
            )
            data[k] = expression
        else:
            data[k] = group_functions[v.get('method', None)](
                v['field'].replace('.', '__')
            )

    return data


def get_chart(id):
    """获取图表数据

    Params:
        user object 用户对象
        id int Chart 模型主键
    """

    chart = cache.get(f'chart_config:{id}', None)
    log.debug(f'chart get from cache: {chart}')
    if chart is None:
        chart = Chart.objects.prefetch_related(
            'metrics', 'dimensions', 'chart_filters'
        ).get(id=id)
        cache.set(f'chart_config:{id}', chart, 600)
        log.debug('cached Chart')

    group = {}
    fields = {}
    for dimension in chart.dimensions.all():
        field = {
            'field': dimension.field,
            'displayName': dimension.display_name,
            'expression': dimension.expression,
        }
        if dimension.method:
            field['method'] = dimension.method
        group[dimension.name] = field

    for metric in chart.metrics.all():
        field = {
            'displayName': metric.display_name,
            'format': metric.format,
        }
        if metric.expression is None:
            field.update({
                'field': metric.field,
                'method': metric.method,
            })
        else:
            field['expression'] = metric.expression
        fields[metric.name] = field

    group_kwargs = get_group_data(group)
    filters = [ft.build() for ft in chart.chart_filters.filter(parent__isnull=True)]
    data = group_statistics_data(
        fields,
        group_kwargs,
        sort_keys=chart.order_by,
        top_max=chart.top_max,
        filters=filters,
        model=apps.get_model(*chart.model.split('__')),
    )
    return data


@bsm_func(login_required=True, name='get_chart', model=Chart)
def get_chart_func(user, id, **kwargs):
    return success_response(get_chart(id))


@bsm_func(
    login_required=True,
    name='set_user_group_object_permission',
    model=UserObjectPermission,
)
def set_user_group_object_permission(
    user, data_id, codename, to_users=None, to_groups=None, **kwargs
):
    """
    指定具体某一条数据给指定用户（组)对应的权限

    Params:
        id 数据 ID
        codename string chart.view_chart
        to_users list 指定给谁（用户 ID）
        to_groups list 组id 列表
    """
    try:
        app_label, perm_code = codename.split('.')
        model_slug = perm_code.split('_')[1]
        content_type = ContentType.objects.get(app_label=app_label, model=model_slug)
    except Exception:
        raise exceptions.BusinessException(
            error_code=exceptions.PARAMETER_FORMAT_ERROR,
            error_data=f'指定的 codename: {codename} 找不到对应的 ContentType',
        )

    try:
        permission = Permission.objects.get(content_type=content_type, codename=perm_code)
    except Exception:
        raise exceptions.BusinessException(
            error_code=exceptions.PARAMETER_FORMAT_ERROR,
            error_data=f'指定的 codename: {codename} 找不到对应的 Permission',
        )

    try:
        content_object = content_type.model_class().objects.get(id=data_id)
    except Exception:
        raise exceptions.BusinessException(
            error_code=exceptions.PARAMETER_FORMAT_ERROR,
            error_data=f'指定的 data_id: {data_id} 找不到对应的数据',
        )

    if not to_users and not to_groups:
        raise exceptions.BusinessException(
            error_code=exceptions.PARAMETER_FORMAT_ERROR, error_data='没有指定对应的用户和组',
        )

    if isinstance(to_users, list):
        if to_users:
            user_qs = get_user_model().objects.filter(id__in=to_users)
            if user_qs:
                UserObjectPermission.objects.filter(
                    content_type=content_type,
                    permission=permission,
                    object_pk=str(content_object.id),
                ).delete()
                assign_perm(codename, user_qs, content_object)
        else:
            UserObjectPermission.objects.filter(
                content_type=content_type,
                permission=permission,
                object_pk=str(content_object.id),
            ).delete()

    if isinstance(to_groups, list):
        if to_groups:
            group_qs = Group.objects.filter(id__in=to_groups)
            if group_qs:
                GroupObjectPermission.objects.filter(
                    content_type=content_type,
                    permission=permission,
                    object_pk=str(content_object.id),
                ).delete()
                assign_perm(codename, group_qs, content_object)
        else:
            GroupObjectPermission.objects.filter(
                content_type=content_type,
                permission=permission,
                object_pk=str(content_object.id),
            ).delete()
