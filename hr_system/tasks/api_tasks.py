from celery import shared_task
from hcs_hr.celery import BaseTask
import time


@shared_task(base=BaseTask)
def create_order(order_info=None):
    if order_info is None:
        order_info = dict()

    print("Сообщение отправлено!")
    time.sleep(2)
    return True
