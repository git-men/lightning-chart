from django.dispatch import receiver
from api_basebone.signals import post_bsm_create
from chart.models import Chart


# @receiver(post_bsm_create, sender=Chart, dispatch_uid='gen_chart')
# def gen_chart(sender, instance: Chart, **kwargs):
#     instance.gen_by_args()
