# Generated by Django 2.2.9 on 2020-06-11 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0010_auto_20200612_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dimensionargs',
            name='chart',
        ),
        migrations.RemoveField(
            model_name='dimensionargs',
            name='template',
        ),
        migrations.RemoveField(
            model_name='dimensiontemplate',
            name='template',
        ),
        migrations.RemoveField(
            model_name='metricargs',
            name='chart',
        ),
        migrations.RemoveField(
            model_name='metricargs',
            name='template',
        ),
        migrations.RemoveField(
            model_name='metrictemplate',
            name='template',
        ),
        migrations.DeleteModel(
            name='ChartTemplate',
        ),
        migrations.DeleteModel(
            name='DimensionArgs',
        ),
        migrations.DeleteModel(
            name='DimensionTemplate',
        ),
        migrations.DeleteModel(
            name='MetricArgs',
        ),
        migrations.DeleteModel(
            name='MetricTemplate',
        ),
    ]
