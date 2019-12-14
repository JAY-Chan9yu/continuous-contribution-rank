#-*- coding: utf-8 -*-
from fabric.contrib.files import append, exists, sed, put
from fabric.api import env, local, run, sudo, settings
import random
import os
import json

PROJECT_NAME = 'sample'
PROJECT_GITHUB = 'https://github.com/JAY-Chan9yu/{}.git'.format(PROJECT_NAME)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DOCKER = 'docker'
STAGING = 'staging'
PRODUCT = 'product'

env.user = 'deploy'
env.target = '' # 베포 타겟


# 배포 환경 (실서버, 개발서버, 도커 ...)
def docker():
    env.target = DOCKER


def staging():
    env.target = STAGING


def prod():
    env.target = PRODUCT


# API 서버
def api():
    if env.target == DOCKER:
        env.hosts = 'bt-api'
    elif env.target == STAGING:
        env.hosts = '개발서버 host'
    elif env.target == PRODUCT:
        env.hosts = '실서버 host'


# 초기 프로젝트 clone 및 관련 폴더생성, 패키지 설치
def init():
    install_package()
    make_project()


# init()으로 프로젝트 배포후, 추가 패키지 설치 및 프로젝트 pull
def dist():
    # 가장 최근 커밋으로 소스를 되돌림 (충돌 방지)
    head = local("git rev-parse HEAD", capture=True)
    run('cd /users/deploy/sample && git reset --hard {}'.format(head))
    # 로컬 프로젝트의 최신 커밋으로
    run('cd /users/deploy/sample && git pull')
    # 필요한 라이브러리 설치
    run('/users/deploy/venv/bin/pip install -r /users/deploy/sample/requirement.txt')

    # 가상환경 실행, 프로젝트 runserver
    run('cd /users/deploy/ && source venv/bin/activate && /users/deploy/sample/./manage.py runserver 0.0.0.0:8888')


# 기본적으로 필요한 패키지 설치
def install_package():
    sudo('apt-get update')
    sudo('apt-get install python3')
    sudo('apt-get install python3-pip')
    sudo('apt-get install build-essential')
    sudo('apt-get install virtualenv virtualenvwrapper')


def make_project():
    ''' private repo(Two-Factor Auth repo) 일 때 '''
    # with settings(prompts={"Username for 'https://github.com': ": "USER_NAME",
    #                        "Password for 'https://jay-chan9yu@github.com': ": TOKEN}):
    run('cd /users/deploy && git clone {}'.format(PROJECT_GITHUB))
    # 가상환경 설치
    run('cd /users/deploy && virtualenv venv')
    # 필요한 라이브러리 설치
    run('/users/deploy/venv/bin/pip install -r /users/deploy/sample/requirement.txt')
