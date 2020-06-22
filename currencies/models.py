from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class CurrencyManager(models.Manager):
    def actual(self):
        now = datetime.now()
        return self.filter(exchangedate_from__gte=now)\
                   .filter(exchangedate_to__lt=now)


class Currency(models.Model):
    USD = "USD"
    EUR = "EUR"
    CURRENCY_CHOICES = (
        (USD, _("United State Dollar")),
        (EUR, _("Euro")),
    )

    name = models.CharField(
        _("Валюта"),
        choices=CURRENCY_CHOICES,
        max_length=128
    )
    buy = models.DecimalField(
        _("Курс покупки"),
        max_digits=10,
        decimal_places=4
    )
    sell = models.DecimalField(
        _("Курс продажи"),
        max_digits=10,
        decimal_places=4
    )
    exchangedate_from = models.DateField(_("Дата с которой действует курс"))
    exchangedate_to = models.DateField(
        _("Дата до которой действует курс"),
        blank=True,
        null=True
    )

    objects = CurrencyManager()

    class Meta:
        verbose_name = _("Курс валюты")
        verbose_name_plural = _("Курс валют")

    def __str__(self):
        return self.name