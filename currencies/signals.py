from datetime import timedelta
import math

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Currency

@receiver(post_save, sender=Currency)
def create_object_update_dates(sender, instance, created, **kwargs):
    if created:

        prev_record = sender.objects.filter(
            name=instance.name,
            exchangedate_from__lt=instance.exchangedate_from
        ).order_by('exchangedate_from').last()

        if prev_record:

            delta = (instance.exchangedate_from - prev_record.exchangedate_to).days

            if math.fabs(delta) > 1:

                prev_record.exchangedate_to = instance.exchangedate_from - timedelta(days=1)
                prev_record.save()


        next_record = sender.objects.filter(
            name=instance.name,
            exchangedate_from__gt=instance.exchangedate_from
        ).order_by('exchangedate_from').first()

        if next_record:

            instance.exchangedate_to = next_record.exchangedate_from - timedelta(days=1)
            instance.save()


@receiver(post_delete, sender=Currency)
def delete_object_update_dates(sender, instance, **kwargs):
    prev_record = sender.objects.filter(
        name=instance.name,
        exchangedate_from__lt=instance.exchangedate_from
    ).order_by('exchangedate_from').last()

    next_record = sender.objects.filter(
        name=instance.name,
        exchangedate_from__gt=instance.exchangedate_from
    ).order_by('exchangedate_from').first()

    if next_record:
        prev_record.exchangedate_to = next_record.exchangedate_from - timedelta(days=1)
    else:
        prev_record.exchangedate_to = None

    prev_record.save()