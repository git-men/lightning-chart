# Generated by Django 2.2.9 on 2020-07-10 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0014_auto_20200630_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimension',
            name='expression',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='表达式'),
        ),
        migrations.AddField(
            model_name='metric',
            name='expression',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='表达式'),
        ),
    ]
