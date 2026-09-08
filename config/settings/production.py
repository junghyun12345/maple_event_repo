"""실서버(EC2)용 설정."""

from .base import *  # noqa

DEBUG = False

# 서버 접속을 허용할 주소. .env 의 ALLOWED_HOSTS 에서 읽습니다.
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# nginx가 HTTPS를 종료하고 뒤로 http로 전달 → Django에 "원래 https였다"고 알림
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# HTTPS에서 폼 제출(로그인·관리자)을 허용할 도메인
CSRF_TRUSTED_ORIGINS = [
    'https://maplemate.life',
    'https://www.maplemate.life',
]

# 보안 쿠키 (https 연결에서만 전송)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS: 브라우저가 앞으로 https로만 접속하도록. 우선 1시간, 안정화되면 늘려도 됨.
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# 프록시 뒤 기본 방어
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
