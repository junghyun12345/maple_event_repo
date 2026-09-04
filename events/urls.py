from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="list"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("write/", views.event_write, name="write"),
    path("upload-image/", views.upload_image, name="upload_image"),  # 본문 이미지 업로드
    path("archive/", views.archive, name="archive"),
    path("events/<slug:slug>/edit/", views.event_edit, name="edit"),
    path("events/<slug:slug>/", views.event_detail, name="detail"),
]
