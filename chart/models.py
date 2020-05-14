from django.db import models
from api_basebone.core.fields import JSONField, BoneImageUrlField


class ChartTemplate(models.Model):
    name = models.CharField(verbose_name='名称', max_length=200, default='')
    image = BoneImageUrlField(verbose_name='示例')

    class Meta:
        verbose_name = '图表模板'
        verbose_name_plural = '图表模板'


class MetricTemplate(models.Model):
    display_name = models.CharField(verbose_name='显示名称', max_length=30)
    name = models.CharField(verbose_name='名称', max_length=20)
    geom = JSONField(verbose_name='geom')
    template = models.ForeignKey(ChartTemplate, verbose_name='模板', related_name='metrics', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '指标模板'
        verbose_name_plural = '指标模板'


class DimensionTemplate(models.Model):
    display_name = models.CharField(verbose_name='显示名称', max_length=30)
    name = models.CharField(verbose_name='名称', max_length=20)
    template = models.ForeignKey(ChartTemplate, verbose_name='模板', related_name='dimensions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '维度模板'
        verbose_name_plural = '维度模板'


class Chart(models.Model):
    name = models.CharField(verbose_name='名称', max_length=200, default='')
    model = models.CharField(verbose_name='模型', max_length=200)


class Metric(models.Model):
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, verbose_name='图表',
                              related_name='metrics')
    display_name = models.CharField(verbose_name='指标显示名称', max_length=30)
    name = models.CharField(verbose_name='指标名', max_length=20)
    field = models.CharField(verbose_name='字段', max_length=30)
    method = models.CharField(verbose_name='聚合函数', max_length=20)
    geom = JSONField(verbose_name='geom')

    class Meta:
        verbose_name = '指标'
        verbose_name_plural = '指标'


class Dimension(models.Model):
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, verbose_name='图表',
                              related_name='dimensions')
    display_name = models.CharField(verbose_name='维度显示名称', max_length=30)
    name = models.CharField(verbose_name='维度名', max_length=20)
    field = models.CharField(verbose_name='字段', max_length=30)
    method = models.CharField(verbose_name='统计精度函数（当field类型时时间时会有）', max_length=20, blank=True)

    class Meta:
        verbose_name = '维度'
        verbose_name_plural = '维度'


class Filter(models.Model):
    TYPE_CONTAINER = 0
    TYPE_CONDITION = 1

    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, verbose_name='图表',
                              related_name='filters')
    type = models.IntegerField('条件类型',
                             choices=((TYPE_CONTAINER, '容器'), (TYPE_CONDITION, '单一条件')))
    parent = models.ForeignKey(
        'self', models.CASCADE, null=True, verbose_name='parent', related_name="children"
    )
    field = models.CharField(verbose_name='字段', max_length=30)
    operator = models.CharField('条件判断符', max_length=20)
    value = models.CharField('条件值', max_length=100)
    layer = models.IntegerField('嵌套层数', default=0)

    class Meta:
        verbose_name = '查询条件'
        verbose_name_plural = '查询条件'
