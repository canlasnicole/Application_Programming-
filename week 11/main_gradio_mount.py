"""
main_gradio_mount.py  ── 1.1 단일 서버
─────────────────────────────────────────────────────
Gradio를 FastAPI에 Mount하여 단일 서버로 실행

  실행 방법:
    python train_model.py          # 먼저 모델 학습
    uvicorn main_gradio_mount:app --reload --port 8000

  접속:
    http://localhost:8000          → FastAPI (REST API)
    http://localhost:8000/gradio   → Gradio UI
    http://localhost:8000/docs     → Swagger UI
─────────────────────────────────────────────────────
"""

import numpy as np
import joblib
import gradio as gr
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ── 1. FastAPI app ─────────────────────────────────
app = FastAPI(
    title="🍷 Wine Prediction API",
    description="RandomForest wine classifier (3 features)",
    version="1.0.0",
)

# ── 2. Load saved model artifacts ──────────────────
model    = joblib.load("model.pkl")
scaler   = joblib.load("scaler.pkl")
selector = joblib.load("selector.pkl")

CLASS_NAMES     = ["class_0", "class_1", "class_2"]
SELECTED_FEATS  = ["flavanoids", "od280/od315_of_diluted_wines", "proline"]

# ── 3. FastAPI endpoints ───────────────────────────
class WineInput(BaseModel):
    flavanoids: float
    od_ratio:   float
    proline:    float

@app.get("/")
def root():
    return {"message": "🍷 Wine Prediction Service", "ui": "/gradio", "docs": "/docs"}

@app.post("/predict")
def predict(data: WineInput):
    x     = np.array([[data.flavanoids, data.od_ratio, data.proline]])
    x_sc  = scaler.transform(x)
    pred  = int(model.predict(x_sc)[0])
    proba = model.predict_proba(x_sc)[0].tolist()
    return {
        "predicted_class" : CLASS_NAMES[pred],
        "class_index"     : pred,
        "probabilities"   : dict(zip(CLASS_NAMES, proba)),
    }

@app.get("/features")
def features():
    return {"selected_features": SELECTED_FEATS}

# ── 4. Gradio UI ───────────────────────────────────
def gradio_predict(flavanoids: float, od_ratio: float, proline: float) -> str:
    x    = np.array([[flavanoids, od_ratio, proline]])
    x_sc = scaler.transform(x)
    pred  = model.predict(x_sc)[0]
    proba = model.predict_proba(x_sc)[0]
    label = CLASS_NAMES[pred]

    bars = ""
    for cls, p in zip(CLASS_NAMES, proba):
        filled = int(p * 20)
        bar    = "█" * filled + "░" * (20 - filled)
        arrow  = " ◀ PREDICTED" if cls == label else ""
        bars  += f"  {cls:8s}  [{bar}]  {p*100:5.1f}%{arrow}\n"

    return (
        f"🍷  Predicted : **{label.upper()}**\n\n"
        f"📊  Probabilities:\n{bars}"
    )

with gr.Blocks(title="Wine Predictor") as gradio_app:
    gr.Markdown("## 🍷 Wine Class Predictor\n단일 서버 (FastAPI Mount) 버전")

    with gr.Row():
        with gr.Column():
            sl1 = gr.Slider(0.34, 5.08, value=2.7,  step=0.01, label="Flavanoids")
            sl2 = gr.Slider(1.27, 4.00, value=2.6,  step=0.01, label="OD280/OD315 of diluted wines")
            sl3 = gr.Slider(278,  1680,  value=746,  step=1,    label="Proline")
            btn = gr.Button("🍷 Predict", variant="primary")
        with gr.Column():
            out = gr.Markdown("_슬라이더를 조절하고 Predict를 클릭하세요._")

    btn.click(fn=gradio_predict, inputs=[sl1, sl2, sl3], outputs=out)
    for sl in [sl1, sl2, sl3]:
        sl.change(fn=gradio_predict, inputs=[sl1, sl2, sl3], outputs=out)

    gr.Markdown(
        "**REST API:** `POST /predict` | **Swagger:** `/docs`\n\n"
        "Features: flavanoids, od280/od315_of_diluted_wines, proline"
    )

# ── 5. Mount Gradio onto FastAPI ───────────────────
app = gr.mount_gradio_app(app, gradio_app, path="/gradio")

# ── 6. Run ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_gradio_mount:app", host="0.0.0.0", port=8000, reload=True)
