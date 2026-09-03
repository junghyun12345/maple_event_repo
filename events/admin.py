from django.contrib import admin

from .models import Event, Reward


class RewardInline(admin.TabularInline):
    """이벤트 편집 화면 안에서 보상을 같이 입력하도록 끼워 넣습니다."""

    model = Reward
    extra = 1  # 빈 입력줄 1개를 기본으로 보여줌


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # 목록 화면에 보일 컬럼들
    list_display = ("title", "category", "status", "start_at", "end_at", "is_published")
    # 오른쪽 필터
    list_filter = ("category", "is_published")
    # 검색창 대상
    search_fields = ("title", "summary_short")
    # 이벤트 편집하면서 보상도 함께 입력
    inlines = [RewardInline]
    # slug는 한글 제목에서 자동 생성하지 않음(설계 방침) → 직접 입력
