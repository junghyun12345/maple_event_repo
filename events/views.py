from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Event


def event_list(request):
    """이벤트 목록. status 파라미터로 진행중/예정/종료를 거릅니다 (기본: 진행중)."""
    now = timezone.now()
    status = request.GET.get("status", "ongoing")
    published = Event.objects.filter(is_published=True)

    if status == "upcoming":  # 예정: 아직 시작 안 함
        events = published.filter(start_at__gt=now)
    elif status == "ended":   # 종료: 종료일이 지남
        events = published.filter(end_at__lt=now)
    else:                     # 진행중(기본): 시작했고, 아직 안 끝났거나 상시
        status = "ongoing"
        events = published.filter(start_at__lte=now).filter(
            Q(end_at__gte=now) | Q(end_at__isnull=True)
        )

    return render(request, "events/event_list.html", {"events": events, "status": status})


def event_detail(request, slug):
    """이벤트 상세. slug로 하나를 찾고, 없으면 404."""
    event = get_object_or_404(Event, slug=slug, is_published=True)
    return render(request, "events/event_detail.html", {"event": event})


def archive(request):
    """지난 이벤트 모음 (종료된 것)."""
    now = timezone.now()
    events = Event.objects.filter(is_published=True, end_at__lt=now)
    return render(request, "events/archive.html", {"events": events})
