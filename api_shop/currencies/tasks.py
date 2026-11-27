from celery import shared_task

from .services import update_usd_exchange_rate


@shared_task
def update_usd_exchange_rate_task():
    return update_usd_exchange_rate()
