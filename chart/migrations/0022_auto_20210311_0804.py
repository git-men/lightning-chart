# Generated by Django 2.2.19 on 2021-03-11 08:04

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0021_auto_20210311_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartcardfilter',
            name='value',
            field=jsonfield.fields.JSONField(default='{{__UNDEFINED__}}', verbose_name='条件值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filter',
            name='value',
            field=jsonfield.fields.JSONField(default='{{__UNDEFINED__}}', verbose_name='条件值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statisticfilter',
            name='value',
            field=jsonfield.fields.JSONField(default='{{__UNDEFINED__}}', verbose_name='条件值'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chartcardfilter',
            name='_value_legacy',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='条件值（已弃用）'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='_value_legacy',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='条件值（已弃用）'),
        ),
        migrations.AlterField(
            model_name='statisticfilter',
            name='_value_legacy',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='条件值（已弃用）'),
        ),
    ]
