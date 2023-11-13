import datetime
import time

from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import F


@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription
    with transaction.atomic():  # оконное фунция для того что написанное внизу или пройдет или нет все вместе

        # select_for_update() не дас доступ базе по тому айдишнику с которым он уже работает
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotated_price=F('service__full_price') -
                            F('service__full_price') *
                            F('plan__discount_percent') / 100).first()
        subscription.price = subscription.annotated_price
        subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)

@shared_task(base=Singleton)
def set_data(subscription_id):
    from services.models import Subscription
    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)
        subscription.data_modified = str(datetime.datetime.now())
        subscription.save()