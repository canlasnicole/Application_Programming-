# 📚 도서관 책대여관리시스템

FastAPI + SQLAlchemy로 구현한 도서관 책 대여 관리 REST API

---

## 🏗️ 프로젝트 구조 (MVC — Like a package)

```
library_v3/
├── main.py              # FastAPI 앱 진입점 (lifespan으로 테이블 생성)
├── database.py          # DB 연결 설정 (engine, SessionLocal, get_db)
├── books/
│   ├── models.py        # Model   — books 테이블 정의 (SQLAlchemy)
│   ├── schemas.py       # View    — 입출력 데이터 검증 (Pydantic)
│   ├── crud.py          # 비즈니스 로직 (ISBN 중복 검증 포함)
│   └── router.py        # Controller — /api/books 엔드포인트
├── members/
│   ├── models.py        # Model   — members 테이블 정의
│   ├── schemas.py       # View    — 이메일 형식·중복 검증
│   ├── crud.py          # 비즈니스 로직
│   └── router.py        # Controller — /api/members 엔드포인트
└── rentals/
    ├── models.py        # Model   — rentals 테이블 정의
    ├── schemas.py       # View    — 입출력 검증
    ├── crud.py          # 비즈니스 로직 (대출·반납·연체 처리)
    └── router.py        # Controller — /api/rentals 엔드포인트
```

### MVC 역할 분리

| 레이어 | 파일 | 역할 |
|--------|------|------|
| Model | `*/models.py` | SQLAlchemy — SQL 데이터 저장·조회 |
| View | `*/schemas.py` | Pydantic — 입출력 데이터 검증·변환 |
| Controller | `*/router.py` | FastAPI — 요청 수신 → 모델 호출 → 응답 반환 |

---

## ⚙️ 설치 및 실행

### 1. 패키지 설치

```bash
pip install fastapi sqlalchemy uvicorn[standard] pydantic[email]
```

### 2. 서버 실행

```bash
cd library_v3
python -m uvicorn main:app --reload
```

### 3. Swagger UI 접속

```
http://127.0.0.1:8000/docs
```

---

## 🌐 API 엔드포인트

### 📖 Books

| Method | URL | 설명 |
|--------|-----|------|
| POST | `/api/books/` | 책 등록 (ISBN 중복 검증) |
| GET | `/api/books/` | 전체 책 목록 조회 |
| GET | `/api/books/available` | 대출 가능한 책만 조회 |
| GET | `/api/books/{book_id}` | 특정 책 조회 |
| PATCH | `/api/books/{book_id}` | 책 정보 수정 |
| DELETE | `/api/books/{book_id}` | 책 삭제 |

### 👤 Members

| Method | URL | 설명 |
|--------|-----|------|
| POST | `/api/members/` | 회원 등록 (이메일 형식·중복 검증) |
| GET | `/api/members/` | 전체 회원 목록 조회 |
| GET | `/api/members/{member_id}` | 특정 회원 조회 |
| PATCH | `/api/members/{member_id}` | 회원 정보 수정 |
| DELETE | `/api/members/{member_id}` | 회원 삭제 |

### 📋 Rentals

| Method | URL | 설명 |
|--------|-----|------|
| POST | `/api/rentals/` | 책 대출 (대출 가능 여부 확인) |
| PATCH | `/api/rentals/{rental_id}/return` | 책 반납 |
| GET | `/api/rentals/` | 전체 대출 기록 조회 |
| GET | `/api/rentals/overdue` | 연체 중인 대출 목록 |
| DELETE | `/api/rentals/{rental_id}` | 대출 기록 삭제 |

---

## 💡 등록 예시 (curl)

```bash
# 책 등록
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "파이썬 완전정복", "author": "홍길동", "isbn": "978-0-1234"}'

# 회원 등록
curl -X POST http://127.0.0.1:8000/api/members/ \
  -H "Content-Type: application/json" \
  -d '{"name": "김철수", "email": "kim@example.com"}'

# 책 대출 (book_id=1, member_id=1)
curl -X POST http://127.0.0.1:8000/api/rentals/ \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "member_id": 1, "due_date": "2025-07-01"}'
```

---

## 🛠️ 기술 스택

| 항목 | 내용 |
|------|------|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Database | SQLite (`library.db`) |
| Server | Uvicorn |
| Python | 3.10+ |

---

## 📝 과제 정보

- 과목: 2026 Spring
- 주제: 도서관 책대여관리시스템
- 구조: FastAPI MVC (Like a package)
- 참고: CRISP-DM 프로세스 기반 설계
