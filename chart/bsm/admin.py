from api_basebone.core.admin import BSMAdmin, register
from .. import models


# @register
# class ChartTemplateAdmin(BSMAdmin):
#     filter = ['name']
#     display = ['name', 'image']
#     form_fields = [
#         'name', 'image',
#         {'name': 'metrics', 'widget': 'InlineForm', 'params': {'canAdd': True}},
#         {'name': 'dimensions', 'widget': 'InlineForm', 'params': {'canAdd': True}},
#     ]
#     inline_actions = ['edit', 'delete']

#     class Meta:
#         model = models.ChartTemplate

@register
class StatisticAdmin(BSMAdmin):
    filter = ['display_name', 'model']
    display = ['display_name', 'model', 'field', 'method', 'prefix', 'postfix']
    form_fields = ['display_name', 'model', 'field', 'method', {'name': 'filters', 'params': {'canAdd': True, 'fields': ['field', 'operator', 'value']}}, 'prefix', 'postfix', {'name': 'parent', 'widget': 'Cascader'}]
    inline_actions = ['edit', 'delete']

    class Meta:
        model = models.Statistic


@register
class ChartCardAdmin(BSMAdmin):
    filter = ['model']
    display = ['model']
    form_fields = ['model', 'field', 'main_chart', 'chart_style', 'primary_metric', 'secondary_metric', {'name': 'filters', 'params': {'canAdd': True, 'fields': ['field', 'operator', 'value']}}, {'name': 'parent', 'widget': 'Cascader'}]
    inline_actions = ['edit', 'delete']

    class Meta:
        model = models.ChartCard


@register
class ChartCardMetric(BSMAdmin):
    form_fields = ['display_name', 'method', 'prefix', 'postfix']

    class Meta:
        model = models.ChartCardMetric
