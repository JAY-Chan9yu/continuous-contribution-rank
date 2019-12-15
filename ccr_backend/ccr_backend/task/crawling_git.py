import os

from celery import Celery
from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime, timedelta

from django.conf import settings

# from users.models import UserGitHub
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.local')

BROKER_URL = settings.REDIS_BROKER_URL
CELERY_RESULT_BACKEND = settings.REDIS_BROKER_URL

app = Celery('task', broker=BROKER_URL)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.update(
#     CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
# )

@app.task
def say_hello():
    """
        Task 테스트 함수
    """
    return "hello ~"


@app.task
def crawling_git_contribution():
    from apps.users.models import UserGitHub
    user_github_qs = UserGitHub.objects.all()

    for user_github in user_github_qs:
        url = "https://github.com/{}".format(user_github.address)
        # test
        print(url)
        print("before count : {}".format(user_github.count))

        # todo : 오늘 체크 했는데 혹시나 또 task가 돌아갈 수 있나? -> Modify 필드 추가하자
        is_commit = get_contribution_status(url)
        if is_commit is True:
            user_github.count += 1
        else:
            user_github.count = 0

        # test
        print("after count : {}".format(user_github.count))
        user_github.save()


def get_contribution_status(url):
    """
        get today contribution status(count)
    """

    soup = BeautifulSoup(request.urlopen(url), 'html.parser')

    # update 할 날짜
    utc_yesterday = datetime.utcnow() - timedelta(days=1)
    date_str = utc_yesterday.date().strftime('%Y-%m-%d')
    print(date_str)

    # contribution 크롤링
    contribution_graph = soup.find('svg', class_='js-calendar-graph-svg')
    today_commit = contribution_graph.find('rect', attrs={"data-date": date_str})

    if int(today_commit.attrs.get('data-count')) > 0:
        return True

    return False
