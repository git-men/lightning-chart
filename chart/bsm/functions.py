import logging

from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from api_basebone.drf.response import success_response
from api_basebone.restful.funcs import bsm_func
from api_basebone.core import exceptions

from chart.models import Chart
from guardian.shortcuts import GroupObjectPermission, assign_perm
from guardian.models import UserObjectPermission

log = logging.getLogger(__name__)


@bsm_func(login_required=True, name='get_chart', model=Chart)
def get_chart(user, id, **kwargs):
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

    self = kwargs.get('view_context')['view']

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
        if dimension.name == 'groupby':
            group[dimension.name] = field
        if dimension.name == 'legend':
            group[dimension.name] = field

    for metric in chart.metrics.all():
        field = {
            'field': metric.field,
            'method': metric.method,
            'expression': metric.expression,
            'displayName': metric.display_name,
            'format': metric.format,
        }
        fields[metric.name] = field

    group_kwargs = self.get_group_data(group)
    filters = [
        {'field': ft.field, 'operator': ft.operator, 'value': ft.value}
        for ft in chart.chart_filters.all()
    ]
    data = self.group_statistics_data(
        fields,
        group_kwargs,
        sort_keys=chart.sort_keys,
        top_max=chart.top_max,
        filters=filters,
    )
    return success_response(data)


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
