import logging

from django.core.cache import cache

from api_basebone.drf.response import success_response
from api_basebone.restful.funcs import bsm_func

from chart.models import Chart

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
