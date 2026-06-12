"""
test_api.py — pytest 기반 API 테스트
Run: pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ─────────────────────────────────────────
# 기본 테스트
# ─────────────────────────────────────────

def test_root():
    """루트 엔드포인트 정상 응답"""
    res = client.get("/")
    assert res.status_code == 200
    assert "project" in res.json()


# ─────────────────────────────────────────
# Sales 테스트
# ─────────────────────────────────────────

def test_get_sales():
    """판매 데이터 조회"""
    res = client.get("/api/sales/?limit=10")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_sales_summary():
    """판매 통계 요약"""
    res = client.get("/api/sales/summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_revenue" in data
    assert "unique_customers" in data


def test_monthly_trend():
    """월별 매출 트렌드 EDA"""
    res = client.get("/api/sales/monthly")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "revenue" in data[0]
    assert "month_num" in data[0]


def test_region_breakdown():
    """지역별 매출 분석 EDA"""
    res = client.get("/api/sales/region")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert "Region" in data[0]
    assert "revenue" in data[0]


def test_search_sales():
    """키워드 검색"""
    res = client.get("/api/sales/search?keyword=Bikes")
    assert res.status_code == 200
    assert "count" in res.json()


def test_get_sale_not_found():
    """존재하지 않는 판매 기록 → 404"""
    res = client.get("/api/sales/9999999")
    assert res.status_code == 404


def test_create_and_delete_sale():
    """판매 기록 생성 후 삭제"""
    payload = {
        "CustomerKey": 1,
        "ProductKey": 1,
        "SalesTerritoryKey": 1,
        "Order_Quantity": 2,
        "Unit_Price": 100.0,
        "Sales_Amount": 200.0,
        "Country_Region": "Test",
        "Region": "Test Region",
        "Category": "Bikes",
        "Subcategory": "Road Bikes",
        "Color": "Red",
        "Date": "2025-01-01",
        "month_num": 1,
        "year_num": 2025,
    }
    res = client.post("/api/sales/", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] == "success"
    new_id = res.json()["id"]

    del_res = client.delete(f"/api/sales/{new_id}")
    assert del_res.status_code == 200


# ─────────────────────────────────────────
# Customers 테스트
# ─────────────────────────────────────────

def test_get_customers():
    """전체 고객 조회"""
    res = client.get("/api/customers/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_top_customers():
    """상위 고객 조회"""
    res = client.get("/api/customers/top?limit=5")
    assert res.status_code == 200
    data = res.json()
    assert len(data) <= 5


def test_churn_risk():
    """이탈 위험 고객 목록"""
    res = client.get("/api/customers/churn-risk")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_clv_tier_valid():
    """CLV 티어 조회 — VIP"""
    res = client.get("/api/customers/clv/VIP")
    assert res.status_code == 200


def test_clv_tier_invalid():
    """CLV 티어 잘못된 값 → 400"""
    res = client.get("/api/customers/clv/INVALID")
    assert res.status_code == 400


def test_rfm_segment_valid():
    """RFM 세그먼트 조회 — Champions"""
    res = client.get("/api/customers/rfm/Champions")
    assert res.status_code == 200


def test_customer_not_found():
    """존재하지 않는 고객 → 404"""
    res = client.get("/api/customers/9999999")
    assert res.status_code == 404


# ─────────────────────────────────────────
# Products 테스트
# ─────────────────────────────────────────

def test_get_products():
    """전체 제품 조회"""
    res = client.get("/api/products/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_top_products():
    """상위 제품 조회"""
    res = client.get("/api/products/top?limit=5")
    assert res.status_code == 200


# ─────────────────────────────────────────
# Predict 테스트
# ─────────────────────────────────────────

def test_model_info():
    """모델 정보 조회"""
    res = client.get("/api/predict/info")
    assert res.status_code == 200
    data = res.json()
    assert "churn_classifier" in data
    assert "sales_regressor" in data
    assert "timeseries" in data


def test_predict_churn():
    """이탈 위험 예측"""
    payload = {
        "Recency": 120,
        "total_orders": 5,
        "total_spend": 3500.0,
        "avg_spend": 700.0,
        "tenure_days": 400,
        "RFM_score": 8,
        "CLV": 120.5,
    }
    res = client.post("/api/predict/churn", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "churn_risk" in data
    assert data["churn_risk"] in [0, 1]
    assert "label" in data


def test_predict_sales():
    """판매 금액 예측"""
    payload = {
        "Recency": 30,
        "total_orders": 10,
        "total_spend": 8000.0,
        "avg_spend": 800.0,
        "tenure_days": 600,
        "RFM_score": 10,
        "CLV": 500.0,
    }
    res = client.post("/api/predict/sales", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "predicted_amount" in data
    assert data["predicted_amount"] >= 0


def test_timeseries_forecast():
    """시계열 예측 — 6개월"""
    res = client.get("/api/predict/timeseries?n_months=6")
    assert res.status_code == 200
    data = res.json()
    assert "historical" in data
    assert "forecast" in data
    assert len(data["forecast"]) == 6


def test_timeseries_max_months():
    """시계열 예측 — 최대 24개월"""
    res = client.get("/api/predict/timeseries?n_months=24")
    assert res.status_code == 200
    assert len(res.json()["forecast"]) == 24


def test_timeseries_invalid_months():
    """시계열 예측 — 범위 초과 → 422"""
    res = client.get("/api/predict/timeseries?n_months=99")
    assert res.status_code == 422
