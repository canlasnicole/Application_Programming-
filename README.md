# 📊 AdventureWorks CRM API

**FastAPI · SQLite · scikit-learn · Hugging Face Spaces**

A full-stack CRM analysis and prediction API built on AdventureWorks sales data. Features a clean MVC architecture with four modules — Sales, Customers, Products, and ML Predictions — plus a Docker-ready deployment config for Hugging Face Spaces.

---

## 🏗️ Project Structure

```
adventureworks/
├── main.py                    # FastAPI app entry point
├── database.py                # SQLite connection & table setup
├── adventureworks.db          # SQLite database
├── AdventureWorks_Sales.xlsx  # Source data
├── requirements.txt
├── Dockerfile
├── test_api.py                # pytest test suite
├── sales/
│   ├── models.py              # SQL queries
│   ├── schemas.py             # Pydantic I/O schemas
│   ├── crud.py                # Business logic
│   └── router.py              # /api/sales endpoints
├── customers/
│   ├── models.py              # RFM / CLV / churn queries
│   ├── schemas.py
│   ├── crud.py
│   └── router.py              # /api/customers endpoints
├── products/
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── router.py              # /api/products endpoints
└── predict/
    ├── models.py              # scikit-learn model training
    ├── schemas.py             # Prediction I/O schemas
    ├── crud.py                # Model loading & inference
    └── router.py              # /api/predict endpoints
```

### MVC Layer Mapping

| Layer | File | Role |
|---|---|---|
| Model | `*/models.py` | SQL data access / ML model training |
| View | `*/schemas.py` | Pydantic validation & serialization |
| Controller | `*/router.py` | Request routing → crud → response |

---

## ⚙️ Setup & Run

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Swagger UI → **http://127.0.0.1:8000/docs**

### Docker

```bash
docker build -t adventureworks-crm .
docker run -p 7860:7860 adventureworks-crm
```

---

## 🌐 API Endpoints

### 📈 Sales

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/sales/` | All sales records |
| GET | `/api/sales/summary` | Revenue & order stats |
| GET | `/api/sales/monthly` | Monthly revenue trend (EDA) |
| GET | `/api/sales/region` | Regional revenue breakdown (EDA) |
| GET | `/api/sales/search?keyword=Bikes` | Keyword search |
| POST | `/api/sales/` | Create sale record |
| PUT | `/api/sales/{id}` | Update sale record |
| DELETE | `/api/sales/{id}` | Delete sale record |

### 👥 Customers

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/customers/` | All customer features |
| GET | `/api/customers/top` | Top customers by spend |
| GET | `/api/customers/churn-risk` | Churn-risk customer list |
| GET | `/api/customers/clv/{tier}` | By CLV tier: `VIP` / `Mid-Value` / `Bargain Hunter` |
| GET | `/api/customers/rfm/{segment}` | By RFM segment: `Champions` / `Loyal` / `At Risk` / `Lost` |

### 🛒 Products

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products/` | All products |
| GET | `/api/products/top` | Top-selling products |

### 🤖 Predict

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/predict/info` | Model info & performance metrics |
| POST | `/api/predict/churn` | Churn risk prediction (Random Forest classifier) |
| POST | `/api/predict/sales` | Purchase amount prediction (Linear Regression) |
| POST | `/api/predict/retrain` | Retrain models on current data |
| GET | `/api/predict/timeseries?n_months=6` | Revenue forecast (up to 24 months) |

---

## 🤖 Prediction Examples

**Churn Risk**
```bash
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

**Sales Amount**
```bash
curl -X POST http://127.0.0.1:8000/api/predict/sales \
  -H "Content-Type: application/json" \
  -d '{
    "Recency": 30,
    "total_orders": 10,
    "total_spend": 8000.0,
    "avg_spend": 800.0,
    "tenure_days": 600,
    "RFM_score": 10,
    "CLV": 500.0
  }'
```

---

## 🧪 Testing

```bash
pip install pytest httpx
pytest test_api.py -v
```

Covers: root, sales CRUD, monthly/region EDA, customer segments, CLV/RFM filters, product queries, churn & sales prediction, timeseries forecasting, and error handling (404 / 400 / 422).

---

## 🛠️ Tech Stack

| | |
|---|---|
| Framework | FastAPI |
| Database | SQLite |
| Data | Pandas, NumPy |
| ML | scikit-learn (RandomForest, LinearRegression) |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Deployment | Docker · Hugging Face Spaces (port 7860) |

---

## 📝 Course Info

- Course: Big Data — Spring 2026, Kyungbok University
- Topic: AdventureWorks CRM Analysis System
- Architecture: FastAPI MVC (package structure)
- Models: Churn classification + Sales amount regression
