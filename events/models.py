from django.db import models
from django.utils import timezone


class Event(models.Model):
    """메이플 이벤트 하나를 나타내는 표(테이블)."""

    class Category(models.TextChoices):
        EVENT = "event", "이벤트"
        UPDATE = "update", "업데이트"
        CASHSHOP = "cashshop", "캐시샵"
        COUPON = "coupon", "쿠폰"

    title = models.CharField("제목", max_length=200)
    slug = models.SlugField(
        "URL 조각",
        max_length=200,
        unique=True,
        help_text="주소에 쓰이는 영문 조각. 한글 자동변환은 안 되니 직접 영문으로 입력.",
    )
    category = models.CharField("카테고리", max_length=20, choices=Category.choices)
    start_at = models.DateTimeField("시작 일시")
    end_at = models.DateTimeField(
        "종료 일시",
        null=True,
        blank=True,
        help_text="종료일 없는 상시 이벤트는 비워둡니다.",
    )
    thumbnail = models.ImageField("썸네일", upload_to="thumbnails/", blank=True)
    summary_short = models.CharField(
        "한 줄 요약", max_length=255, help_text="목록 카드에 보이는 한 줄."
    )
    summary_three = models.TextField(
        "3줄 요약", help_text="줄바꿈으로 구분. 두 줄이나 네 줄이 될 수도 있음."
    )
    body = models.TextField(
        "상세 본문",
        blank=True,
        help_text="마크다운. 비우면 '상세히 보기' 버튼이 숨겨집니다.",
    )
    source_url = models.URLField("원문 링크", blank=True)
    is_published = models.BooleanField("발행", default=False)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "이벤트"
        verbose_name_plural = "이벤트"
        ordering = ["-start_at"]

    def __str__(self):
        return self.title

    @property
    def status(self):
        now = timezone.now()
        if self.start_at > now:
            return "예정"
        if self.end_at and self.end_at < now:
            return "종료"
        return "진행중"

    @property
    def days_left(self):
        if not self.end_at:
            return None
        delta = self.end_at - timezone.now()
        return delta.days if delta.days >= 0 else None


class Reward(models.Model):
    """이벤트 하나에 딸린 보상. 한 이벤트에 여러 개(1:N)."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="rewards",
        verbose_name="이벤트",
    )
    name = models.CharField("보상 이름", max_length=200)
    quantity = models.CharField("수량", max_length=100, blank=True)
    condition = models.CharField("획득 조건", max_length=255, blank=True)
    order = models.PositiveIntegerField("정렬 순서", default=0)

    class Meta:
        verbose_name = "보상"
        verbose_name_plural = "보상"
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.event.title})"
