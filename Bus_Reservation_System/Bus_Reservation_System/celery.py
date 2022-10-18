from __future__ import absolute_import

import os
from celery import Celery



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bus_Reservation_System.settings")
app = Celery("Bus_Reservation_System")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request)) 