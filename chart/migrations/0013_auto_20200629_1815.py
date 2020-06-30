# Generated by Django 2.2.9 on 2020-06-29 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0012_auto_20200627_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='sort_type',
            field=models.CharField(blank=True, choices=[('asce', '升序'), ('desc', '降序')], default=None, max_length=50, null=True, verbose_name='排序类型'),
        ),
    ]