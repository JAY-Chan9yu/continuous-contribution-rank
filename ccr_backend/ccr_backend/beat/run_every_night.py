from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

from django.conf import settings

BROKER_URL = settings.REDIS_BROKER_URL
CELERY_RESULT_BACKEND = settings.REDIS_BROKER_URL

app = Celery('beat', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE={
        'say_hello-every-seconds': {
            'task': 'task.crawling_git.crawling_git_contribution',
            #'schedule': crontab(minute=0, hour=6),  # 매일 오전 6시에 실행
            'schedule': timedelta(seconds=5),  # test용
            'args': ()
        },
    }
)




