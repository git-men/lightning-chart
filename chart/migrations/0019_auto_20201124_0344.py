# Generated by Django 2.2.9 on 2020-11-24 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0018_auto_20201109_0458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chartcard',
            name='chart_y',
        ),
        migrations.RemoveField(
            model_name='chartcard',
            name='chart_y_method',
        ),
        migrations.AlterField(
            model_name='chartcard',
            name='chart_x',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='图表维度'),
        ),
        migrations.AlterField(
            model_name='chartcard',
            name='chart_x_method',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='图表维度函数'),
        ),
    ]
