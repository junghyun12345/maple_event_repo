"""
공통 설정 (base). 로컬/서버 공통으로 쓰는 값들.
로컬은 config/settings/local.py, 서버는 config/settings/production.py 가
이 파일을 import 해서 필요한 부분만 덮어씁니다.
"""

from pathlib import Path

import environ

# settings/base.py 기준으로 세 단계 위가 프로젝트 최상위(manage.py가 있는 곳)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# .env 에서 비밀 값 읽기
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')  # 기본 False. local.py에서 True로 덮어씀
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 내 앱
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': env.db(),
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# 정적 파일 (CSS/JS 등). 서버에서는 collectstatic으로 STATIC_ROOT에 모아 nginx가 서빙.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 업로드 이미지(미디어 파일)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 로그인
LOGIN_URL = 'events:login'
LOGIN_REDIRECT_URL = 'events:list'
LOGOUT_REDIRECT_URL = 'events:list'
