"""실서버(EC2)용 설정."""

from .base import *  # noqa

DEBUG = False

# 서버 접속을 허용할 주소. .env 의 ALLOWED_HOSTS 에서 읽습니다 (예: 서버 IP).
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# 아직 HTTPS(도메인) 전이라 SSL 강제 리다이렉트는 켜지 않습니다.
# 나중에 도메인+certbot 붙이면 아래를 켭니다:
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# 프록시(nginx) 뒤에 있을 때 클릭재킹/콘텐츠 스니핑 방어
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
