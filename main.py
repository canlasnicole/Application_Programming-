"""
main.py — FastAPI 앱 진입점
AdventureWorks CRM — MVC (Like a package) 구조
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables

from sales.router     import router as sales_router
from customers.router import router as customers_router
from products.router  import router as products_router
from predict.router   import router as predict_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    create_tables()
    print("🚀 AdventureWorks CRM API 시작!")
    yield
    # shutdown


app = FastAPI(
    title="📊 AdventureWorks CRM API",
    description="""
    AdventureWorks 판매 데이터 분석 및 예측 API
    
    - **Sales**: 판매 데이터 CRUD + EDA (월별/지역별 분석)
    - **Customers**: RFM 세그먼트 / CLV 티어 / 이탈 위험 분석
    - **Products**: 제품별 매출 분석
    - **Predict**: 이탈 예측 (분류) + 구매 금액 예측 (회귀)
    """,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales_router)
app.include_router(customers_router)
app.include_router(products_router)
app.include_router(predict_router)


@app.get("/", tags=["Info"])
def root():
    return {
        "project": "AdventureWorks CRM Analysis",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "sales":     "/api/sales",
            "customers": "/api/customers",
            "products":  "/api/products",
            "predict":   "/api/predict",
        }
    }
