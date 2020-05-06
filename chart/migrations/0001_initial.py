# Generated by Django 2.2 on 2020-04-30 16:07

import api_basebone.core.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, verbose_name='名称')),
                ('model', models.CharField(max_length=200, verbose_name='模型')),
            ],
        ),
        migrations.CreateModel(
            name='DimensionTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=30, verbose_name='显示名称')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
            ],
            options={
                'verbose_name': '维度模板',
                'verbose_name_plural': '维度模板',
            },
        ),
        migrations.CreateModel(
            name='MetricTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=30, verbose_name='显示名称')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('geom', api_basebone.core.fields.JSONField(verbose_name='geom')),
            ],
            options={
                'verbose_name': '指标模板',
                'verbose_name_plural': '指标模板',
            },
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=30, verbose_name='指标显示名称')),
                ('name', models.CharField(max_length=20, verbose_name='指标名')),
                ('field', models.CharField(max_length=30, verbose_name='字段')),
                ('method', models.CharField(max_length=20, verbose_name='聚合函数')),
                ('geom', api_basebone.core.fields.JSONField(verbose_name='geom')),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='chart.Chart', verbose_name='图表')),
            ],
            options={
                'verbose_name': '指标',
                'verbose_name_plural': '指标',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, '容器'), (1, '单一条件')], verbose_name='条件类型')),
                ('field', models.CharField(max_length=30, verbose_name='字段')),
                ('operator', models.CharField(max_length=20, verbose_name='条件判断符')),
                ('value', models.CharField(max_length=100, verbose_name='条件值')),
                ('layer', models.IntegerField(default=0, verbose_name='嵌套层数')),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='chart.Chart', verbose_name='图表')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='chart.Filter', verbose_name='parent')),
            ],
            options={
                'verbose_name': '查询条件',
                'verbose_name_plural': '查询条件',
            },
        ),
        migrations.CreateModel(
            name='Dimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=30, verbose_name='维度显示名称')),
                ('name', models.CharField(max_length=20, verbose_name='维度名')),
                ('field', models.CharField(max_length=30, verbose_name='字段')),
                ('method', models.CharField(max_length=20, verbose_name='统计精度函数（当field类型时时间时会有）')),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dimensions', to='chart.Chart', verbose_name='图表')),
            ],
            options={
                'verbose_name': '维度',
                'verbose_name_plural': '维度',
            },
        ),
        migrations.CreateModel(
            name='ChartTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, verbose_name='名称')),
                ('image', models.URLField(verbose_name='示例')),
                ('dimensions', models.ManyToManyField(to='chart.DimensionTemplate', verbose_name='指标')),
                ('metrics', models.ManyToManyField(to='chart.MetricTemplate', verbose_name='指标')),
            ],
            options={
                'verbose_name': '图表模板',
                'verbose_name_plural': '图表模板',
            },
        ),

    ]
