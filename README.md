# Focus Memo

> **기록을 검색 가능한 데이터로**
> 비번 같은 건 일부만 기억나도, 키워드/카테고리로 빠르게 찾는 메모앱

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| 메모 CRUD | 작성 · 조회 · 수정 · 삭제 |
| 자동 키워드 추출 | 저장 시 본문에서 핵심 단어 자동 추출 (상위 5개) |
| 통합 검색 | 본문 + 키워드 동시 검색 (부분 일치) |
| 카테고리 필터 | 생활 / 업무 / 학습 / 임시 / 이벤트 |
| 정렬 | 최신순 / 오래된순 |
| 페이지네이션 | 10개씩 페이지 분할 |
| 회원 인증 | 회원가입 · 로그인 · 로그아웃, 내 메모만 조회 |

---

## 기술 스택

- **Backend** : Python 3.14, Django 6.0.1
- **Database** : SQLite3
- **Frontend** : HTML/CSS (Bootstrap 5 일부 사용)
- **인증** : Django 내장 Auth

---

## 프로젝트 구조

```
My Second Project/
├── focus/              # Django 프로젝트 설정
│   ├── settings.py
│   └── urls.py
├── memo/               # 메모 앱
│   ├── models.py       # Memo, Category 모델 + 키워드 추출 로직
│   ├── views.py        # CRUD 뷰 + 검색/필터
│   ├── forms.py        # MemoForm
│   └── urls.py
├── users/              # 회원 앱
│   ├── views.py        # 회원가입
│   └── urls.py
├── templates/
│   ├── memo/           # 목록, 상세, 작성/수정 템플릿
│   ├── registration/   # 로그인 템플릿
│   └── users/          # 회원가입 템플릿
├── .env                # 환경변수 (git 미포함)
├── requirements.txt
└── manage.py
```

---

## 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/dongjebag59-dev/Innovative-Memo-App.git
cd Innovative-Memo-App
```

### 2. 가상환경 생성 및 패키지 설치

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env` 파일을 프로젝트 루트에 생성합니다.

```
SECRET_KEY=여기에_시크릿키_입력
```

### 4. 마이그레이션 및 서버 실행

```bash
python manage.py migrate
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 접속

---

## 핵심 구현 포인트

### 자동 키워드 추출 (`memo/models.py`)

메모 저장 시 `save()` 오버라이드를 통해 본문에서 핵심 단어를 자동 추출합니다.

```python
def save(self, *args, **kwargs):
    if self.content:
        kws = extract_keywords(self.content, top_n=5)
        self.keywords = ",".join(kws)
    super().save(*args, **kwargs)
```

### 검색 (Q 객체 활용, `memo/views.py`)

본문과 키워드를 동시에 검색합니다.

```python
memos = memos.filter(
    Q(content__icontains=q) | Q(keywords__icontains=q)
)
```

### 접근 제어

`@login_required` 데코레이터로 인증된 사용자만 메모 기능에 접근 가능하며,
`author=request.user` 필터로 본인 메모만 조회됩니다.

---

## 카테고리 목록

| 아이콘 | 이름 |
|--------|------|
| 🏠 | 생활 |
| 💼 | 업무 |
| 📚 | 학습 |
| 📝 | 임시 |
| 🎉 | 이벤트 |
