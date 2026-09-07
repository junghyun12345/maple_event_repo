"""
WSGI config for config project.
서버(gunicorn)에서 이 파일을 통해 앱을 구동합니다 → production 설정 사용.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
