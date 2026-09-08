# 🍁 메이플 이벤트 요약 사이트

메이플스토리 진행 이벤트를 한 곳에 모아 요약해 보여주는 웹사이트입니다.
운영자가 이벤트를 직접 작성·요약해 올리고, 방문자는 진행중·예정·종료 이벤트와 보상을 빠르게 확인합니다.

> **Live demo:** http://43.200.15.23
> (개인 서버라 비용 절감을 위해 가끔 꺼져 있을 수 있습니다.)

---

## 주요 기능

**방문자용**
- 이벤트 목록 (진행중 / 예정 / 종료 상태 필터)
- 이벤트 상세 — 3줄 요약(팝업) · 마크다운 본문 · 보상 목록 · 원문 링크
- 지난 이벤트(아카이브) 페이지
- 이미지 강조형 카드 UI, 반응형 레이아웃

**운영자용 (로그인 필요)**
- 사이트에서 직접 로그인 후 이벤트 작성 · 수정
- 마크다운 에디터(EasyMDE) + 본문 이미지 드래그 업로드
- 보상 여러 개 입력 (inline formset, 동적 추가)
- 작성 중 자동 임시저장 (localStorage)
- Django 관리자 페이지

---

## 기술 스택

| 구분 | 사용 기술 |
|---|---|
| 백엔드 | Django 6.1, Python 3.12 |
| 데이터베이스 | PostgreSQL |
| 프론트 | Django 템플릿, Tailwind CSS + DaisyUI, EasyMDE, marked.js |
| 인프라 | AWS EC2 (Ubuntu, ARM), Nginx, Gunicorn, systemd |

---

## 설계 포인트

- **설정 분리** — `config/settings/`를 `base / local / production`으로 나눠, 로컬과 실서버 설정을 안전하게 분리 (실서버 DEBUG 실수 방지).
- **비밀 값 분리** — `django-environ`으로 `SECRET_KEY`·DB 비밀번호를 `.env`에서 로드, 저장소에는 커밋하지 않음.
- **상태는 저장하지 않고 계산** — 이벤트의 진행중/예정/종료는 시작·종료 일시로 계산하는 프로퍼티로 처리해 별도 갱신(크론) 불필요.
- **1:N 모델링** — 이벤트(Event) 1개에 보상(Reward) N개를 ForeignKey + inline formset으로 구성.

---

## 로컬 실행

```bash
git clone <this-repo>
cd maple_event_repo

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# .env 파일 생성 (.env.example 참고)
#   SECRET_KEY=...
#   DEBUG=True
#   ALLOWED_HOSTS=127.0.0.1,localhost
#   DATABASE_URL=postgres://USER:PASSWORD@127.0.0.1:5432/DBNAME

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

http://127.0.0.1:8000 접속.

---

## 배포 개요 (AWS EC2)

`로컬에서 git push` → `서버에서 git pull → migrate → collectstatic → gunicorn 재시작`.
Nginx가 정적/미디어 파일을 서빙하고 나머지 요청을 Gunicorn(WSGI)으로 전달합니다.

---

## 스크린샷

_(목록 / 상세 / 작성 화면 캡처를 여기에 추가)_
