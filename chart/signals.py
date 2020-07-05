import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from chart.models import Chart
from django.core.cache import cache

log = logging.getLogger(__name__)

@receiver(post_save, sender=Chart, dispatch_uid='clean_chart_cache_by_save')
def clean_chart_cache_by_save(sender, instance, **kwargs):
    cache.delete(f'chart_config:{instance.id}')
    log.debug('remove chart cache')


@receiver(post_delete, sender=Chart, dispatch_uid='clean_chart_cache_by_delete')
def clean_chart_cache_by_delete(sender, instance, **kwargs):
    cache.delete(f'chart_config:{instance.id}')