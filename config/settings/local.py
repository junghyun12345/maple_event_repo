"""로컬 개발용 설정."""

from .base import *  # noqa

DEBUG = True

# 로컬에서는 내 컴퓨터에서만 접속
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
