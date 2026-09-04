from django.contrib import admin

from .models import Event, Reward


class RewardInline(admin.TabularInline):
    model = Reward
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "start_at", "end_at", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("title", "summary_short")
    inlines = [RewardInline]
