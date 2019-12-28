import os
import time

from celery import Celery
from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime, timedelta

from django.conf import settings

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


@app.task
def update_commit_history(address):
    """
        처음 아이디가 입력 되었을때 (modified 값 보고)
        total_commit, last commit update
    """
    from apps.github.models import GitHubCommit, GitHubAddress

    utc_now = datetime.utcnow()

    # TODO: GitHubCommit 생성 정리 (생성 방식이 이상함.. 없는거 알면서 get)
    try:
        github_commit = GitHubCommit.objects.filter(address=address).get()

    except GitHubCommit.DoesNotExist:
        print("GitHubCommit Does Not Exist.")
        address = GitHubAddress.objects.filter(id=address).first()
        if address is None:
            return

        github_commit = GitHubCommit.objects.create(
            created=utc_now,
            address=address
        )

    last_commit = None
    total_commit_cnt = 0  # github 페이지에 노출되는 최대 커밋수(1년)
    continuous_commit_cnt = 0  # 오늘 이전으로 연속된 커밋수
    max_continuous_commit_cnt = 0  # 최대 연속 커밋수
    check_continuous_cnt = 0  # 최대 연속 커밋수 체크

    try:
        url = "https://github.com/{}".format(github_commit.address.name)
        source_code_from_URL = request.urlopen(url)
        soup = BeautifulSoup(source_code_from_URL, 'html.parser')

        date_str = utc_now.date().strftime('%Y-%m-%d')
        contribution_graph = soup.find('svg', class_='js-calendar-graph-svg')

        is_continuous = True
        while True:
            today_commit = contribution_graph.find('rect', attrs={"data-date": date_str})

            # github 잔디에서 가져올 데이터가 없는경우
            if today_commit is None:
                break

            commit_cnt = int(today_commit.attrs.get('data-count'))
            if commit_cnt > 0:
                total_commit_cnt += 1
                check_continuous_cnt += 1

                if last_commit is None:
                    last_commit = datetime.strptime(last_commit, '%Y-%m-%d')

                if is_continuous is True:
                    continuous_commit_cnt += 1

            if commit_cnt == 0:
                # 최대 연속 커밋 수
                if check_continuous_cnt > max_continuous_commit_cnt:
                    max_continuous_commit_cnt = check_continuous_cnt

                # 오늘 이전으로 연속적으로 커밋했는지 체크 끝
                if is_continuous is True:
                    is_continuous = False

                check_continuous_cnt = 0

            utc_now -= timedelta(days=1)
            date_str = utc_now.date().strftime('%Y-%m-%d')

    except Exception as e:
        # TODO: log 남기기
        print(e)

    update_fields = ['total_commit', 'last_commit', 'continuous_commit', 'max_continuous_commit']
    github_commit.last_commit = last_commit
    github_commit.max_continuous_commit = max_continuous_commit_cnt
    github_commit.continuous_commit = continuous_commit_cnt
    github_commit.total_commit = total_commit_cnt
    github_commit.save(update_fields=update_fields)
