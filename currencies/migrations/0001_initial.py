# Generated by Django 2.0.13 on 2020-06-22 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('USD', 'Unated State Dollar'), ('EUR', 'Euro')], max_length=128, verbose_name='Валюта')),
                ('buy', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Курс покупки')),
                ('sell', models.DecimalField(decimal_places=4, max_digits=10, verbose_name='Курс продажи')),
                ('exchangedate_from', models.DateField(verbose_name='Дата с которой действует курс')),
                ('exchangedate_to', models.DateField(verbose_name='Дата до которой действует курс')),
            ],
            options={
                'verbose_name': 'Курс валюты',
                'verbose_name_plural': 'Курс валют',
            },
        ),
    ]
