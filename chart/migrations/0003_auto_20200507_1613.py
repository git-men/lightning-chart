# Generated by Django 2.2 on 2020-05-07 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0002_load_intial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimension',
            name='method',
            field=models.CharField(blank=True, max_length=20, verbose_name='统计精度函数（当field类型时时间时会有）'),
        ),
    ]
