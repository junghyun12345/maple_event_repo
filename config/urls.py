from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events.urls")),  # 사이트 첫 화면부터는 events 앱이 담당
]
