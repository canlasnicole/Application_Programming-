"""
api.py  ── 1.2 별도 서버 : FastAPI 서버
─────────────────────────────────────────────────────
  실행 방법 (터미널 1):
    python train_model.py
    uvicorn api:app --reload --port 8000

  접속:
    http://localhost:8000/docs   → Swagger UI
    http://localhost:8000/predict (POST)
─────────────────────────────────────────────────────
"""

import numpy as np
import joblib
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated

# ── 1. FastAPI app ─────────────────────────────────
app = FastAPI(
    title="🍷 Wine Prediction API",
    description="RandomForest wine classifier — 별도 서버 버전",
    version="1.0.0",
)

# CORS (Gradio 클라이언트에서 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 2. Dependency Injection: 모델 로드 ─────────────
#    교수님 자료 Section 2 (Injection) 패턴 적용
class ModelService:
    """모델 관련 객체를 한 곳에서 관리 (DI 컨테이너)"""
    def __init__(self):
        self.model    = joblib.load("model.pkl")
        self.scaler   = joblib.load("scaler.pkl")
        self.selector = joblib.load("selector.pkl")
        self.classes  = ["class_0", "class_1", "class_2"]
        self.features = ["flavanoids", "od280/od315_of_diluted_wines", "proline"]
        print("✅  ModelService loaded via Dependency Injection")

# 싱글턴 인스턴스
_model_service = ModelService()

def get_model_service() -> ModelService:
    """Depends를 통한 의존성 주입"""
    return _model_service

# ── 3. Pydantic schemas ────────────────────────────
class WineInput(BaseModel):
    flavanoids: float
    od_ratio:   float   # od280/od315_of_diluted_wines
    proline:    float

    model_config = {
        "json_schema_extra": {
            "examples": [{"flavanoids": 3.06, "od_ratio": 3.92, "proline": 1065.0}]
        }
    }

class PredictionResult(BaseModel):
    predicted_class : str
    class_index     : int
    probabilities   : dict
    features_used   : list

# ── 4. Endpoints ───────────────────────────────────
@app.get("/")
def root():
    return {
        "service"  : "🍷 Wine Prediction API",
        "version"  : "1.0.0",
        "endpoints": ["/predict", "/features", "/health", "/docs"],
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/features")
def get_features(svc: Annotated[ModelService, Depends(get_model_service)]):
    """선택된 피처 정보 반환"""
    return {"selected_features": svc.features, "n_features": len(svc.features)}

@app.post("/predict", response_model=PredictionResult)
def predict(
    data : WineInput,
    svc  : Annotated[ModelService, Depends(get_model_service)],
):
    """
    와인 클래스 예측
    - flavanoids       : 0.34 ~ 5.08
    - od_ratio         : 1.27 ~ 4.00
    - proline          : 278  ~ 1680
    """
    x     = np.array([[data.flavanoids, data.od_ratio, data.proline]])
    x_sc  = svc.scaler.transform(x)
    pred  = int(svc.model.predict(x_sc)[0])
    proba = svc.model.predict_proba(x_sc)[0].tolist()

    return PredictionResult(
        predicted_class = svc.classes[pred],
        class_index     = pred,
        probabilities   = dict(zip(svc.classes, proba)),
        features_used   = svc.features,
    )

# ── 5. Run ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
