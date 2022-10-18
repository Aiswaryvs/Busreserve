from logging import Logger
from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)




# @shared_task
# def sleepy(duration):
#     sleep(duration)
#     return None

@shared_task
def send_mail_task():
    logger.info("inside send mail task")
    send_mail('working of celery','testing with celery',
             "98aiswaryaaishu@gmail.com",
            ["aiswaryaaishu0001@gmail.com"],
            fail_silently = False,
            )
    print("mail send")
    return None


