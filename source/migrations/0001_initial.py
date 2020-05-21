# Generated by Django 2.2 on 2020-05-09 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=200, verbose_name='路径')),
            ],
            options={
                'verbose_name': '请求模板',
                'verbose_name_plural': '请求模板',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='名称')),
                ('url_prefix', models.CharField(default='https://example.com', max_length=200, verbose_name='请求地址前缀')),
                ('app_key', models.CharField(max_length=100, verbose_name='App Key')),
                ('app_secret', models.CharField(max_length=100, verbose_name='App Secret')),
            ],
            options={
                'verbose_name': '数据源',
                'verbose_name_plural': '数据源',
            },
        ),
        migrations.CreateModel(
            name='TemplateHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=30, verbose_name='键')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.RequestTemplate', verbose_name='模板')),
            ],
            options={
                'verbose_name': '请求头',
                'verbose_name_plural': '请求头',
            },
        ),
        migrations.AddField(
            model_name='requesttemplate',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.Source', verbose_name='数据源'),
        ),
    ]
