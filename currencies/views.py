from django.shortcuts import render
from django.db.models import Max, F

from .models import Currency

# Create your views here.


def index(request):
    currencies = Currency.objects.raw('''
        SELECT id, name, buy, sell, MAX(exchangedate_from) AS latest_date
        FROM currencies_currency
        GROUP BY name'''
    )

    return render(request, 'currencies/index.html', {'currencies': currencies})


def detail(request, name):
    history = Currency.objects.filter(name=name).order_by('exchangedate_from')
    return render(request, 'currencies/detail.html', {'history': history, 'title': name})
