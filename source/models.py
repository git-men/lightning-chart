from django.db import models


class Source(models.Model):
    name = models.CharField('名称', max_length=30)
    url_prefix = models.CharField('请求地址前缀', default='https://example.com', max_length=200)
    app_key = models.CharField('App Key', max_length=100)
    app_secret = models.CharField('App Secret', max_length=100)

    class Meta:
        verbose_name = '数据源'
        verbose_name_plural = verbose_name


class RequestTemplate(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, verbose_name='数据源')
    path = models.CharField('路径', max_length=200)

    class Meta:
        verbose_name = '请求模板'
        verbose_name_plural = verbose_name


class TemplateHeader(models.Model):
    template = models.ForeignKey(RequestTemplate, on_delete=models.CASCADE, verbose_name='模板')
    key = models.CharField('键', max_length=30)

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = verbose_name
