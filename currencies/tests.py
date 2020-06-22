from datetime import datetime, timedelta

from django.test import TestCase
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed

from .models import Currency


class CurrencyTestCase(TestCase):
    def setUp(self):
        signals = [
            pre_save,
            post_save,
            pre_delete,
            post_delete,
            m2m_changed
        ]
        restore = {}
        for signal in signals:
            restore[signal] = signal.receivers
            signal.receivers = []

        Currency.objects.create(
            name='USD',
            buy=24.4500,
            sell=24.9500,
            exchangedate_from=datetime.strptime('2019-12-30', "%Y-%m-%d").date(),
            exchangedate_to=datetime.strptime('2020-01-02', "%Y-%m-%d").date(),
        )
        Currency.objects.create(
            name='USD',
            buy=24.5500,
            sell=24.8500,
            exchangedate_from=datetime.strptime('2020-01-03', "%Y-%m-%d").date(),
            exchangedate_to=datetime.strptime('2020-01-14', "%Y-%m-%d").date(),
        )
        Currency.objects.create(
            name='USD',
            buy=25.2500,
            sell=25.7500,
            exchangedate_from=datetime.strptime('2020-01-15', "%Y-%m-%d").date(),
            exchangedate_to=datetime.strptime('2020-01-29', "%Y-%m-%d").date(),
        )
        Currency.objects.create(
            name='USD',
            buy=26.9500,
            sell=27.1000,
            exchangedate_from=datetime.strptime('2020-01-30', "%Y-%m-%d").date(),
            exchangedate_to=datetime.strptime('2020-03-20', "%Y-%m-%d").date(),
        )

        for signal, receivers in restore.items():
            signal.receivers = receivers


    def test_add_today_kurs_exchangedate_to(self):
        today_kurs = Currency.objects.create(
            name='USD',
            buy=28.1500,
            sell=28.3000,
            exchangedate_from=datetime.now().date(),
        )
        prev_record = Currency.objects.filter(
            name=today_kurs.name,
            exchangedate_from__lt=today_kurs.exchangedate_from
        ).order_by('exchangedate_from').last()
        self.assertEqual(today_kurs.exchangedate_to, None)

    def test_add_today_kurs_prev_record_exchangedate_to(self):
        today_kurs = Currency.objects.create(
            name='USD',
            buy=28.1500,
            sell=28.3000,
            exchangedate_from=datetime.now().date(),
        )
        prev_record = Currency.objects.filter(
            name=today_kurs.name,
            exchangedate_from__lt=today_kurs.exchangedate_from
        ).order_by('exchangedate_from').last()
        self.assertEqual(prev_record.exchangedate_to, today_kurs.exchangedate_from - timedelta(days=1))

    def test_insert_kurs_prev_record_exchangedate_to(self):
        kurs = Currency.objects.create(
            name='USD',
            buy=28.1500,
            sell=28.3000,
            exchangedate_from=datetime.strptime('2020-01-18', "%Y-%m-%d").date(),
        )
        prev_record = Currency.objects.filter(
            name=kurs.name,
            exchangedate_from__lt=kurs.exchangedate_from
        ).order_by('exchangedate_from').last()

        self.assertEqual(prev_record.exchangedate_to, datetime.strptime('2020-01-17', "%Y-%m-%d").date())

    def test_insert_kurs_exchangedate_to(self):
        kurs = Currency.objects.create(
            name='USD',
            buy=28.1500,
            sell=28.3000,
            exchangedate_from=datetime.strptime('2020-01-18', "%Y-%m-%d").date(),
        )

        self.assertEqual(kurs.exchangedate_to, datetime.strptime('2020-01-29', "%Y-%m-%d").date())

    def test_delete_kurs_previous_exchangedate_to(self):
        delete_kurs = Currency.objects.get(
            name='USD',
            buy=24.5500,
            sell=24.8500,
            exchangedate_from=datetime.strptime('2020-01-03', "%Y-%m-%d").date(),
            exchangedate_to=datetime.strptime('2020-01-14', "%Y-%m-%d").date()
        )
        delete_kurs.delete()

        prev_record = Currency.objects.filter(
            name=delete_kurs.name,
            exchangedate_from__lt=delete_kurs.exchangedate_from
        ).order_by('exchangedate_from').last()
        next_record = Currency.objects.filter(
            name=delete_kurs.name,
            exchangedate_from__gt=delete_kurs.exchangedate_from
        ).order_by('exchangedate_from').first()

        self.assertEqual(prev_record.exchangedate_to, datetime.strptime('2020-01-14', "%Y-%m-%d").date())

    def test_delete_kurs_previous_exchangedate_to_empty(self):
        delete_kurs = Currency.objects.get(
            name='USD',
            buy=26.9500,
            sell=27.1000,
            exchangedate_from=datetime.strptime('2020-01-30', "%Y-%m-%d").date(),
            exchangedate_to=datetime.strptime('2020-03-20', "%Y-%m-%d").date(),
        )
        delete_kurs.delete()

        prev_record = Currency.objects.filter(
            name=delete_kurs.name,
            exchangedate_from__lt=delete_kurs.exchangedate_from
        ).order_by('exchangedate_from').last()
        next_record = Currency.objects.filter(
            name=delete_kurs.name,
            exchangedate_from__gt=delete_kurs.exchangedate_from
        ).order_by('exchangedate_from').first()

        self.assertEqual(prev_record.exchangedate_to, None)
