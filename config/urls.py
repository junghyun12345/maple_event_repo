from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 관리자 주소를 기본 /admin/ 대신 추측 어려운 경로로 숨김 (자동 공격 봇 차단)
    path("maple-manager-7x93/", admin.site.urls),
    path("", include("events.urls")),
]

# 개발 중에는 Django가 업로드된 이미지(/media/)를 직접 서빙합니다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
