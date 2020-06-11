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
