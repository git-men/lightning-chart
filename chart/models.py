from django.db import models
from django.apps import apps
from django.db.models import Sum, Count, Avg, Max, Min
from django.db.models.functions import Coalesce

from api_basebone.core.fields import JSONField, BoneImageUrlField
from api_basebone.utils.queryset import GManager
from puzzle import component_resolver
from puzzle.models import Block


# class ChartTemplate(models.Model):
#     name = models.CharField(verbose_name='名称', max_length=200, default='')
#     image = BoneImageUrlField(verbose_name='示例')

#     class Meta:
#         verbose_name = '图表模板'
#         verbose_name_plural = '图表模板'


# class MetricTemplate(models.Model):
#     name = models.CharField(verbose_name='名称', max_length=20)
#     display_name = models.CharField(verbose_name='显示名称', max_length=30)
#     geom = JSONField(verbose_name='geom')
#     template = models.ForeignKey(ChartTemplate, verbose_name='模板', related_name='metrics', on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = '指标模板'
#         verbose_name_plural = '指标模板'


# class DimensionTemplate(models.Model):
#     name = models.CharField(verbose_name='名称', max_length=20)
#     display_name = models.CharField(verbose_name='显示名称', max_length=30)
#     required = models.BooleanField('必填', default=True)
#     template = models.ForeignKey(ChartTemplate, verbose_name='模板', related_name='dimensions', on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = '维度模板'
#         verbose_name_plural = '维度模板'


@component_resolver('Chart')
def chart_resolver(block: Block):
    from chart.bsm.functions import get_chart
    if block.chart is None:
        return None
    chart = Chart.objects.render_get([
        'id', 'template_name', 'name', 'model', 'sort_keys', 'top_max',
        'metrics.id',
        'metrics.chart',
        'metrics.display_name',
        'metrics.name',
        'metrics.field',
        'metrics.expression',
        'metrics.method',
        'metrics.format',
        'metrics.geom',
        'dimensions.id',
        'dimensions.chart',
        'dimensions.display_name',
        'dimensions.name',
        'dimensions.field',
        'dimensions.expression',
        'dimensions.method',
        'chart_filters.id',
        'chart_filters.chart',
        'chart_filters.type',
        'chart_filters.parent',
        'chart_filters.field',
        'chart_filters.operator',
        'chart_filters.value',
        'chart_filters.layer',
    ], id=block.chart.id)
    data = get_chart(block.chart.id)
    return {
        'chart': chart,
        'data': data,
    }


class Chart(models.Model):
    template_name = models.CharField('模板', max_length=100, null=True, blank=True)
    name = models.CharField(verbose_name='名称', max_length=200, default='')
    model = models.CharField(verbose_name='模型', max_length=200)
    sort_keys = JSONField(verbose_name='排序字段', default=[])
    top_max = models.PositiveIntegerField('显示前几条', default=None, null=True)
    block = models.OneToOneField(Block, verbose_name='渲染结点', null=True, on_delete=models.CASCADE)

    objects = GManager()
    # def gen_by_args(self):
    #     self.gen_metrics()
    #     self.gen_dimensions()

    # def gen_metrics(self):
    #     if not self.template:
    #         return

    #     metrics = {m.name: m for m in self.metrics.all()}
    #     metric_args = {m.template.name: m for m in self.metric_args.select_related('template').all()}
    #     update_keys = metrics.keys() & metric_args.keys()
    #     delete_keys = metrics.keys() - metric_args.keys()
    #     create_keys = metric_args.keys() - metrics.keys()

    #     update_list = [metric for name, metric in metrics.items() if name in update_keys]
    #     for metric in update_list:
    #         arg = metric_args[metric.name]
    #         metric.field = arg.field
    #         metric.method = arg.method
    #         metric.display_name = arg.display_name
    #         metric.format = arg.format
    #         metric.geom = arg.template.geom

    #     delete_list = [metric for name, metric in metrics.items() if name in delete_keys]

    #     create_list = [Metric(
    #         field=arg.field,
    #         method=arg.method,
    #         format=arg.format,
    #         name=arg.template.name,
    #         geom=arg.template.geom,
    #         display_name=arg.display_name,
    #         chart=self,
    #     ) for name, arg in metric_args.items() if name in create_keys]

    #     Metric.objects.bulk_create(create_list)
    #     Metric.objects.bulk_update(update_list, fields=['field', 'method', 'geom', 'display_name', 'format'])
    #     Metric.objects.filter(id__in=[d.id for d in delete_list]).delete()

    # def gen_dimensions(self):
    #     if not self.template:
    #         return

    #     dimensions = {m.name: m for m in self.dimensions.all()}
    #     dimension_args = {m.template.name: m for m in self.dimension_args.select_related('template').all()}
    #     update_keys = dimensions.keys() & dimension_args.keys()
    #     delete_keys = dimensions.keys() - dimension_args.keys()
    #     create_keys = dimension_args.keys() - dimensions.keys()

    #     update_list = [dimension for name, dimension in dimensions.items() if name in update_keys]
    #     for dimension in update_list:
    #         arg = dimension_args[dimension.name]
    #         dimension.field = arg.field
    #         dimension.method = arg.method
    #         dimension.display_name = arg.display_name

    #     delete_list = [dimension for name, dimension in dimensions.items() if name in delete_keys]

    #     create_list = [Dimension(
    #         field=arg.field,
    #         method=arg.method,
    #         name=arg.template.name,
    #         display_name=arg.display_name,
    #         chart=self,
    #     ) for name, arg in dimension_args.items() if name in create_keys]

    #     Dimension.objects.bulk_create(create_list)
    #     Dimension.objects.bulk_update(update_list, fields=['field', 'method', 'display_name'])
    #     Dimension.objects.filter(id__in=[d.id for d in delete_list]).delete()


class Metric(models.Model):
    chart = models.ForeignKey(
        Chart, on_delete=models.CASCADE, verbose_name='图表', related_name='metrics'
    )
    display_name = models.CharField(verbose_name='指标名称', max_length=30)
    name = models.CharField(verbose_name='指标名', max_length=20)
    field = models.CharField(verbose_name='字段', max_length=100)
    expression = models.CharField(
        verbose_name='表达式', max_length=500, null=True, blank=True
    )
    method = models.CharField(verbose_name='聚合函数', max_length=20, null=True, blank=True)
    format = models.CharField(verbose_name='格式', max_length=50, default='{}')
    geom = JSONField(verbose_name='geom')

    class Meta:
        verbose_name = '指标'
        verbose_name_plural = '指标'


# class MetricArgs(models.Model):
#     chart = models.ForeignKey(Chart, on_delete=models.CASCADE, verbose_name='图表', related_name='metric_args')
#     template = models.ForeignKey(MetricTemplate, on_delete=models.CASCADE, verbose_name='指标模板', related_name='args')
#     field = models.CharField(verbose_name='字段', max_length=100)
#     method = models.CharField(verbose_name='聚合函数', max_length=20, null=True, blank=True)
#     format = models.CharField(verbose_name='格式', max_length=50, default='{}')
#     display_name = models.CharField(verbose_name='指标名称', max_length=30)

#     class Meta:
#         verbose_name = '指标参数'
#         verbose_name_plural = verbose_name
#         # unique_together = ('chart', 'template')


class Dimension(models.Model):
    chart = models.ForeignKey(
        Chart, on_delete=models.CASCADE, verbose_name='图表', related_name='dimensions'
    )
    display_name = models.CharField(verbose_name='维度名称', max_length=30)
    name = models.CharField(verbose_name='维度名', max_length=20)
    field = models.CharField(verbose_name='字段', max_length=100)
    expression = models.CharField(
        verbose_name='表达式', max_length=500, null=True, blank=True
    )
    method = models.CharField(
        verbose_name='统计精度函数（当field类型时时间时会有）', max_length=20, blank=True, null=True
    )

    class Meta:
        verbose_name = '维度'
        verbose_name_plural = '维度'


# class DimensionArgs(models.Model):
#     chart = models.ForeignKey(Chart, on_delete=models.CASCADE, verbose_name='图表', related_name='dimension_args')
#     template = models.ForeignKey(DimensionTemplate, on_delete=models.CASCADE, verbose_name='维度模板', related_name='args')
#     field = models.CharField(verbose_name='字段', max_length=100)
#     method = models.CharField(verbose_name='聚合函数', max_length=20, blank=True, null=True)
#     display_name = models.CharField(verbose_name='维度名称', max_length=30)

#     class Meta:
#         verbose_name = '指标参数'
#         verbose_name_plural = verbose_name
#         # unique_together = ('chart', 'template')


class BaseFilter(models.Model):
    field = models.CharField(verbose_name='字段', max_length=100)
    operator = models.CharField('条件判断符', max_length=20)
    value = models.CharField('条件值', max_length=100)

    def build(self):
        return {'field': self.field, 'operator': self.operator, 'value': self.value}

    class Meta:
        abstract = True


class Filter(BaseFilter):
    TYPE_CONTAINER = 0
    TYPE_CONDITION = 1

    type = models.IntegerField(
        '条件类型', choices=((TYPE_CONTAINER, '容器'), (TYPE_CONDITION, '单一条件'))
    )
    parent = models.ForeignKey(
        'self', models.CASCADE, null=True, verbose_name='parent', related_name="children"
    )
    chart = models.ForeignKey(
        Chart, on_delete=models.CASCADE, verbose_name='图表', related_name='chart_filters'
    )
    layer = models.IntegerField('嵌套层数', default=0)

    class Meta:
        verbose_name = '查询条件'
        verbose_name_plural = '查询条件'


class Statistic(Block):
    display_name = models.CharField('名称', max_length=30)
    model = models.CharField('模型', max_length=200)
    field = models.CharField('字段', max_length=100)
    method = models.CharField('聚合函数', max_length=20, choices=[
        ['Sum', '累加'],
        ['Count', '计数'],
        ['Avg', '平均值'],
        ['Max', '最大值'],
        ['Min', '最小值'],
    ])
    prefix = models.CharField('前缀', max_length=10, default='', blank=True)
    postfix = models.CharField('后缀', max_length=10, default='', blank=True)

    def save(self, *args, **kwargs):
        self.component = 'Statistic'
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = '统计'
        verbose_name_plural = verbose_name


class StatisticFilter(BaseFilter):
    statistic = models.ForeignKey(
        Statistic, on_delete=models.CASCADE, verbose_name='统计', related_name='filters')

    class Meta:
        verbose_name = '查询条件'
        verbose_name_plural = verbose_name


methods = {
    'Sum': Sum,
    'Count': Count,
    'Avg': Avg,
    'Max': Max,
    'Min': Min,
}


@component_resolver('Statistic')
def statistic_resolver(block: Block):
    statistic = Statistic.objects.get(id=block.id)
    model = apps.get_model(*statistic.model.split('__'))
    return {
        'prefix': statistic.prefix,
        'postfix': statistic.postfix,
        'display_name': statistic.display_name,
        'result': model.objects.filter(*[s.build() for s in statistic.filters.all()]).all().aggregate(result=Coalesce(methods[statistic.method](statistic.field), 0))['result'],
    }
