# Generated by Django 2.0.13 on 2020-06-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0003_auto_20200622_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='exchangedate_to',
            field=models.DateField(blank=True, null=True, verbose_name='Дата до которой действует курс'),
        ),
    ]
