# 📊 AdventureWorks CRM API

FastAPI + SQLite + scikit-learn 기반 판매 데이터 분석 및 예측 API

---

## 🏗️ 프로젝트 구조 (MVC — Like a package)

```
adventureworks/
├── main.py              # FastAPI 앱 진입점
├── database.py          # DB 연결 설정 (SQLite)
├── adventureworks.db    # 데이터베이스 파일
├── AdventureWorks_Sales.xlsx
├── sales/
│   ├── models.py        # Model      — SQL 데이터 저장·조회
│   ├── schemas.py       # View       — Pydantic 입출력 검증
│   ├── crud.py          # 비즈니스 로직
│   └── router.py        # Controller — /api/sales 엔드포인트
├── customers/
│   ├── models.py        # RFM / CLV / 이탈 위험 조회
│   ├── schemas.py
│   ├── crud.py
│   └── router.py        # /api/customers 엔드포인트
├── products/
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── router.py        # /api/products 엔드포인트
└── predict/
    ├── models.py        # scikit-learn 모델 학습
    ├── schemas.py       # 예측 입출력 스키마
    ├── crud.py          # 모델 로딩 및 예측 처리
    └── router.py        # /api/predict 엔드포인트
```

### MVC 역할 분리

| 레이어 | 파일 | 역할 |
|--------|------|------|
| Model | `*/models.py` | SQL 데이터 저장·조회 / ML 모델 학습 |
| View | `*/schemas.py` | Pydantic — 입출력 데이터 검증·변환 |
| Controller | `*/router.py` | FastAPI — 요청 수신 → crud 호출 → 응답 반환 |

---

## ⚙️ 설치 및 실행

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
Huggingface: https://huggingface.co/spaces/canlasnicole/adventureworks-gradio
Swagger UI: **http://127.0.0.1:8000/docs**

---

## 🌐 API 엔드포인트

### 📈 Sales (판매 데이터 CRUD + EDA)

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/sales/` | 전체 판매 데이터 |
| GET | `/api/sales/summary` | 전체 통계 요약 |
| GET | `/api/sales/monthly` | 월별 매출 트렌드 (EDA) |
| GET | `/api/sales/region` | 지역별 매출 분석 (EDA) |
| GET | `/api/sales/search?keyword=Bikes` | 키워드 검색 |
| POST | `/api/sales/` | 판매 기록 생성 |
| PUT | `/api/sales/{id}` | 판매 기록 수정 |
| DELETE | `/api/sales/{id}` | 판매 기록 삭제 |

### 👥 Customers (고객 분석)

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/customers/` | 전체 고객 피처 |
| GET | `/api/customers/top` | 상위 고객 (지출 기준) |
| GET | `/api/customers/churn-risk` | 이탈 위험 고객 |
| GET | `/api/customers/clv/VIP` | CLV 티어별 (VIP / Mid-Value / Bargain Hunter) |
| GET | `/api/customers/rfm/Champions` | RFM 세그먼트별 (Champions / Loyal / At Risk / Lost) |

### 🛒 Products

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/products/` | 전체 제품 목록 |
| GET | `/api/products/top` | 상위 판매 제품 |

### 🤖 Predict (머신러닝 예측)

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/predict/info` | 모델 정보 및 성능 지표 |
| POST | `/api/predict/churn` | 이탈 위험 예측 (RandomForest 분류) |
| POST | `/api/predict/sales` | 구매 금액 예측 (Linear Regression 회귀) |

---

## 🤖 예측 API 사용 예시

```bash
# 이탈 위험 예측
curl -X POST http://127.0.0.1:8000/api/predict/churn \
  -H "Content-Type: application/json" \
  -d '{
    "Recency": 120,
    "total_orders": 5,
    "total_spend": 3500.0,
    "avg_spend": 700.0,
    "tenure_days": 400,
    "RFM_score": 8,
    "CLV": 120.5
  }'
```

---

## 🛠️ 기술 스택

| 항목 | 내용 |
|------|------|
| Framework | FastAPI |
| Database | SQLite |
| Data | Pandas, NumPy |
| ML | scikit-learn (RandomForest, LinearRegression) |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## 📝 과제 정보

- 과목: 2026 Spring
- 주제: AdventureWorks CRM 분석 시스템
- 구조: FastAPI MVC (Like a package)
- 모델: 이탈 예측 (분류) + 판매 금액 예측 (회귀)

---

## 🧪 테스트 실행

```bash
pip install pytest httpx
pytest test_api.py -v
```

## 🤖 모델 재학습

서버 실행 중:
```
POST http://127.0.0.1:8000/api/predict/retrain
```

또는 직접:
```bash
python -c "from predict.crud import retrain_all; retrain_all()"
```

## 📈 시계열 예측

```
GET http://127.0.0.1:8000/api/predict/timeseries?n_months=6
```
