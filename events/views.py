from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import EventForm, RewardFormSet
from .models import Event


def event_list(request):
    """이벤트 목록. status 파라미터로 진행중/예정/종료를 거릅니다 (기본: 진행중)."""
    now = timezone.now()
    status = request.GET.get("status", "ongoing")
    published = Event.objects.filter(is_published=True)

    if status == "upcoming":
        events = published.filter(start_at__gt=now)
    elif status == "ended":
        events = published.filter(end_at__lt=now)
    else:
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


@login_required
def event_write(request):
    """새 이벤트 작성 (로그인 필요)."""
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        formset = RewardFormSet(request.POST, prefix="rewards")
        if form.is_valid() and formset.is_valid():
            event = form.save()
            formset.instance = event
            formset.save()
            return redirect("events:detail", slug=event.slug)
    else:
        form = EventForm()
        formset = RewardFormSet(prefix="rewards")
    return render(request, "events/event_form.html", {"form": form, "formset": formset, "is_edit": False})


@login_required
def event_edit(request, slug):
    """기존 이벤트 수정 (로그인 필요)."""
    event = get_object_or_404(Event, slug=slug)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        formset = RewardFormSet(request.POST, instance=event, prefix="rewards")
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("events:detail", slug=event.slug)
    else:
        form = EventForm(instance=event)
        formset = RewardFormSet(instance=event, prefix="rewards")
    return render(request, "events/event_form.html", {"form": form, "formset": formset, "is_edit": True, "event": event})


@login_required
@require_POST
def upload_image(request):
    """본문 에디터에서 올린 이미지를 저장하고 주소를 돌려줍니다 (EasyMDE용)."""
    f = request.FILES.get("image")
    if not f:
        return JsonResponse({"error": "이미지가 없습니다."}, status=400)
    path = default_storage.save(f"body/{f.name}", f)
    return JsonResponse({"url": default_storage.url(path)})
