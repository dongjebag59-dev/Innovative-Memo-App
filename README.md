# Innovative Memo App

> **기록을 검색 가능한 데이터로**
> 잊어버린 비밀번호도, 일부만 기억나는 단어도 — 동의어 검색으로 빠르게 찾는 스마트 메모앱

**라이브 데모:** [https://djpark99.pythonanywhere.com](https://djpark99.pythonanywhere.com)

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| 메모 CRUD | 작성 · 조회 · 수정 · 삭제 |
| 자동 키워드 추출 | 저장 시 본문에서 핵심 단어 자동 추출 (상위 5개) |
| **한국어 동의어 검색** | "비번" 검색 시 "비밀번호", "password"도 함께 검색 |
| 카테고리 필터 | 생활 / 업무 / 학습 / 임시 / 이벤트 |
| **사용자 태그** | `#태그` 형식으로 자유롭게 분류 |
| **상단 고정(Pin)** | 중요한 메모를 목록 최상단에 고정 |
| **내용 잠금(Secret)** | 민감한 메모를 블러 처리 — 클릭 시 공개 |
| 정렬 | 최신순 / 오래된순 |
| 페이지네이션 | 10개씩 페이지 분할 |
| 검색어 하이라이트 | 검색 결과에서 일치 단어를 시각적으로 강조 |
| 회원 인증 | 회원가입 · 로그인 · 로그아웃, 내 메모만 조회 |

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | Python 3.13, Django 6.0.1 |
| Database | SQLite3 (로컬) |
| Frontend | HTML5/CSS3 (CSS 변수 기반 디자인 시스템) |
| 인증 | Django 내장 Auth |
| 정적 파일 | WhiteNoise |
| 배포 | PythonAnywhere |
| CI/CD | GitHub Actions |
| 컨테이너 | Docker + docker-compose + Nginx (로컬 프로덕션용) |

---

## 프로젝트 구조

```
Innovative-Memo-App/
├── focus/                   # Django 프로젝트 설정
│   ├── settings.py          # 환경변수 기반 설정 (DEBUG, DB, HTTPS)
│   └── urls.py
├── memo/                    # 메모 앱
│   ├── models.py            # Memo 모델 + 키워드 추출 + pin/secret 필드
│   ├── views.py             # CRUD + 동의어 검색 + 핀 토글
│   ├── forms.py             # MemoForm
│   ├── synonyms.py          # 한국어 동의어 사전 (expand_query)
│   ├── urls.py
│   └── templatetags/
│       └── text_filters.py  # highlight, split 커스텀 필터
├── users/                   # 회원 앱
│   ├── views.py             # 회원가입
│   └── urls.py
├── templates/
│   ├── base.html            # 공통 레이아웃 (CSS 변수, 헤더, 플래시 메시지)
│   ├── auth_base.html       # 로그인/회원가입 전용 카드 레이아웃
│   ├── memo/                # 목록, 상세, 작성/수정 템플릿
│   ├── registration/        # 로그인 템플릿
│   └── users/               # 회원가입 템플릿
├── nginx/
│   └── default.conf         # Nginx 설정 (docker-compose 전용)
├── terraform/
│   └── main.tf              # AWS EC2 인프라 코드 (참고용)
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions CI (push 시 자동 테스트)
├── Dockerfile.compose       # docker-compose 전용 이미지
├── docker-compose.yml       # Nginx + Django + PostgreSQL
├── Procfile                 # Railway용 시작 명령
├── railway.toml             # Railway 배포 설정
├── requirements.txt
└── manage.py
```

---

## 로컬 실행 (개발)

### 1. 저장소 클론

```bash
git clone https://github.com/dongjebag59-dev/Innovative-Memo-App.git
cd Innovative-Memo-App
```

### 2. 가상환경 생성 및 패키지 설치

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성합니다.

```
SECRET_KEY=여기에_시크릿키_입력
DEBUG=True
```

> 시크릿키 생성: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 4. 마이그레이션 및 서버 실행

```bash
python manage.py migrate
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 접속

---

## 로컬 실행 (docker-compose)

PostgreSQL + Nginx + Django를 한 번에 실행합니다.

```bash
# .env 파일에 아래 항목 추가
POSTGRES_PASSWORD=비밀번호
ALLOWED_HOSTS=localhost 127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost

docker-compose up --build
```

`http://localhost` 로 접속

---

## 핵심 구현 포인트

### 한국어 동의어 검색 (`memo/synonyms.py`)

"비번"을 검색하면 "비밀번호", "password"도 자동으로 함께 검색됩니다.

```python
SYNONYM_MAP = {
    "비번": ["비밀번호", "password"],
    "통장": ["계좌", "계좌번호"],
    "이메일": ["메일", "email"],
    # ... 20개 이상의 쌍
}

def expand_query(q: str) -> list[str]:
    terms = {q}
    if q.lower() in SYNONYM_MAP:
        terms.update(SYNONYM_MAP[q.lower()])
    return list(terms)
```

### 상단 고정 & 비밀 잠금 (`memo/models.py`)

```python
is_pinned = models.BooleanField(default=False, verbose_name="상단 고정")
is_secret = models.BooleanField(default=False, verbose_name="내용 잠금")
```

- **Pin**: 고정된 메모는 항상 목록 맨 위에 표시 (`order_by("-is_pinned", "-created_at")`)
- **Secret**: 내용을 CSS blur 처리 → 클릭하면 JavaScript로 즉시 공개

### 자동 키워드 추출 (`memo/models.py`)

```python
def save(self, *args, **kwargs):
    if self.content:
        kws = extract_keywords(self.content, top_n=5)
        self.keywords = ",".join(kws)
    super().save(*args, **kwargs)
```

### 검색어 하이라이트 (`memo/templatetags/text_filters.py`)

XSS를 방지하면서 검색어를 `<mark>` 태그로 감쌉니다.

```python
@register.filter(needs_autoescape=True)
def highlight(text, query, autoescape=True):
    escaped = conditional_escape(str(text))
    pattern = re.compile(re.escape(str(query)), re.IGNORECASE)
    result = pattern.sub(lambda m: f'<mark>{conditional_escape(m.group())}</mark>', escaped)
    return mark_safe(result)
```

---

## 카테고리

| 아이콘 | 이름 |
|--------|------|
| 🏠 | 생활 |
| 💼 | 업무 |
| 📚 | 학습 |
| 📝 | 임시 |
| 🎉 | 이벤트 |

---

## 배포 (PythonAnywhere)

현재 **[djpark99.pythonanywhere.com](https://djpark99.pythonanywhere.com)** 에 배포 중입니다.

| 설정 항목 | 값 |
|-----------|-----|
| Python 버전 | 3.13 |
| 가상환경 | `/home/djpark99/Innovative-Memo-App/venv` |
| 정적 파일 URL | `/static/` |
| 정적 파일 경로 | `/home/djpark99/Innovative-Memo-App/staticfiles` |

코드 업데이트 방법:

```bash
# PythonAnywhere Bash 콘솔에서
cd ~/Innovative-Memo-App
git pull origin main
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

이후 **Web 탭 → Reload** 버튼 클릭

---

## CI/CD

`main` 브랜치에 push하면 GitHub Actions가 자동으로 테스트를 실행합니다.

```
push → 패키지 설치 → python manage.py check
```

테스트 통과 후 PythonAnywhere에 수동으로 `git pull` 하여 배포합니다.
