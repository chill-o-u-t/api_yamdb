import re
from datetime import datetime
from celery import Celery
from celery.schedules import crontab

app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        get_year()
    )


@app.task
def get_year():
    return datetime.now().year


SYMBOLS = re.compile('[\w.@+-@./+-]+')

print(SYMBOLS)
