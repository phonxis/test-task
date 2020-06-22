from django.contrib import admin

from .models import Currency
# Register your models here.


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'buy',
        'sell',
        'exchangedate_from',
        'exchangedate_to'
    )
    ordering = ('exchangedate_from', )
