# Generated by Django 2.0.13 on 2020-06-22 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='exchangedate_to',
            field=models.DateField(blank=True, verbose_name='Дата до которой действует курс'),
        ),
    ]
