from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Event, Reward


class Command(BaseCommand):
    help = "테스트용 이벤트 5개(진행중/예정/종료 섞어서)를 생성합니다."

    def handle(self, *args, **options):
        now = timezone.now()
        data = [
            {
                "slug": "chuseok-fullmoon",
                "title": "추석 보름달 출석 이벤트",
                "category": Event.Category.EVENT,
                "start_at": now - timedelta(days=2),
                "end_at": now + timedelta(days=12),
                "thumbnail": "thumbnails/seed1.png",
                "summary_short": "보름 동안 매일 접속하고 보상 받기",
                "summary_three": "매일 접속 시 출석 도장\n7일·14일 개근 보너스\n보름달 코인으로 교환",
                "body": "## 이벤트 안내\n매일 접속해서 도장을 찍으세요.\n\n- 7일 개근: 강화 주문서\n- 14일 개근: 보름달 의자",
                "rewards": [("보름달 의자", "1개", "14일 개근"), ("주문서 15%", "5장", "7일 개근")],
            },
            {
                "slug": "starforce-15",
                "title": "스타포스 15성 강화 이벤트",
                "category": Event.Category.EVENT,
                "start_at": now - timedelta(days=1),
                "end_at": now + timedelta(days=6),
                "thumbnail": "thumbnails/seed4.png",
                "summary_short": "파괴 방지 + 성공 확률 상승",
                "summary_three": "10~15성 파괴 방지\n성공 확률 30% 상승\n기간 중 상시 적용",
                "body": "",
                "rewards": [("파괴 방지", "무제한", "10~15성")],
            },
            {
                "slug": "autumn-update",
                "title": "가을 업데이트: 단풍 숲 신규 지역",
                "category": Event.Category.UPDATE,
                "start_at": now + timedelta(days=5),
                "end_at": now + timedelta(days=40),
                "thumbnail": "thumbnails/seed3.png",
                "summary_short": "새 사냥터와 보스가 열립니다",
                "summary_three": "신규 지역 '단풍 숲'\n신규 보스 '단풍 정령왕'\n레벨 200+ 입장 가능",
                "body": "## 신규 지역\n단풍 숲이 열립니다.",
                "rewards": [],
            },
            {
                "slug": "cashshop-autumn",
                "title": "캐시샵 가을 코디 세트",
                "category": Event.Category.CASHSHOP,
                "start_at": now - timedelta(days=10),
                "end_at": None,  # 상시
                "thumbnail": "thumbnails/seed2.png",
                "summary_short": "한정 가을 코디가 상시 판매",
                "summary_three": "단풍 망토\n도토리 모자\n낙엽 이펙트",
                "body": "",
                "rewards": [("단풍 망토", "1개", "구매 시")],
            },
            {
                "slug": "chuseok-coupon",
                "title": "추석 기념 쿠폰",
                "category": Event.Category.COUPON,
                "start_at": now - timedelta(days=20),
                "end_at": now - timedelta(days=5),  # 종료
                "thumbnail": "thumbnails/seed5.png",
                "summary_short": "종료된 추석 쿠폰 이벤트",
                "summary_three": "쿠폰 번호 입력 시 성장의 비약\n1인 1회\n종료됨",
                "body": "",
                "rewards": [("성장의 비약", "10개", "쿠폰 입력")],
            },
        ]

        for d in data:
            rewards = d.pop("rewards")
            obj, created = Event.objects.get_or_create(
                slug=d["slug"], defaults={**d, "is_published": True}
            )
            if created:
                for i, (name, qty, cond) in enumerate(rewards):
                    Reward.objects.create(event=obj, name=name, quantity=qty, condition=cond, order=i)
                self.stdout.write(self.style.SUCCESS(f"생성: {obj.title}"))
            else:
                self.stdout.write(f"이미 있음(건너뜀): {obj.title}")

        self.stdout.write(self.style.SUCCESS("완료. http://127.0.0.1:8000/ 에서 확인하세요."))
