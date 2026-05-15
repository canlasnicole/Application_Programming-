"""
app_gradio.py  ── 1.2 별도 서버 : Gradio 클라이언트
─────────────────────────────────────────────────────
  실행 방법 (터미널 2, api.py 실행 후):
    python app_gradio.py

  접속:
    http://localhost:7860   → Gradio UI
─────────────────────────────────────────────────────
"""

import requests
import gradio as gr

API_URL = "http://localhost:8000"   # FastAPI 서버 주소

CLASS_NAMES    = ["class_0", "class_1", "class_2"]
CLASS_EMOJI    = {"class_0": "🍷", "class_1": "🫙", "class_2": "🌿"}
CLASS_DESC     = {
    "class_0": "Barolo — 풀바디, 높은 탄닌, 진한 루비색",
    "class_1": "Grignolino — 미디엄바디, 가벼운 타닌",
    "class_2": "Barbera — 산도 높음, 낮은 타닌, 밝은 색",
}

# ── Gradio 예측 함수 (API 호출) ────────────────────
def gradio_predict(flavanoids: float, od_ratio: float, proline: float) -> str:
    payload = {
        "flavanoids": flavanoids,
        "od_ratio"  : od_ratio,
        "proline"   : proline,
    }
    try:
        resp = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
        resp.raise_for_status()
        result = resp.json()
    except requests.exceptions.ConnectionError:
        return "❌ **FastAPI 서버에 연결할 수 없습니다.**\n`uvicorn api:app --port 8000` 을 먼저 실행하세요."
    except Exception as e:
        return f"❌ 오류: {str(e)}"

    label = result["predicted_class"]
    proba = result["probabilities"]

    bars = ""
    for cls in CLASS_NAMES:
        p      = proba.get(cls, 0.0)
        filled = int(p * 20)
        bar    = "█" * filled + "░" * (20 - filled)
        arrow  = " ◀ PREDICTED" if cls == label else ""
        bars  += f"  {cls:8s}  [{bar}]  {p*100:5.1f}%{arrow}\n"

    emoji = CLASS_EMOJI.get(label, "🍷")
    desc  = CLASS_DESC.get(label, "")

    return (
        f"## {emoji}  Predicted : **{label.upper()}**\n\n"
        f"> {desc}\n\n"
        f"**📊 Class Probabilities:**\n```\n{bars}```\n\n"
        f"*API: `POST {API_URL}/predict`*"
    )

# ── Gradio UI ──────────────────────────────────────
with gr.Blocks(title="Wine Predictor — Client") as demo:

    gr.Markdown(
        "## 🍷 Wine Class Predictor\n"
        "**별도 서버 버전** — FastAPI(`api.py`) 서버에 REST 요청\n\n"
        f"API 서버: `{API_URL}`"
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🔬 Input Features")
            sl1 = gr.Slider(0.34, 5.08, value=2.7,  step=0.01, label="Flavanoids",
                            info="Range: 0.34 – 5.08")
            sl2 = gr.Slider(1.27, 4.00, value=2.6,  step=0.01, label="OD280/OD315 of diluted wines",
                            info="Range: 1.27 – 4.00")
            sl3 = gr.Slider(278,  1680,  value=746,  step=1,    label="Proline",
                            info="Range: 278 – 1680")
            btn = gr.Button("🍷 Predict", variant="primary", size="lg")

        with gr.Column():
            gr.Markdown("### 📊 Prediction Result")
            out = gr.Markdown("_슬라이더를 조절하고 Predict 버튼을 클릭하세요._")

    btn.click(fn=gradio_predict, inputs=[sl1, sl2, sl3], outputs=out)
    for sl in [sl1, sl2, sl3]:
        sl.change(fn=gradio_predict, inputs=[sl1, sl2, sl3], outputs=out)

    gr.Markdown(
        "---\n"
        "**Features selected:** flavanoids · od280/od315_of_diluted_wines · proline  \n"
        "**Model:** RandomForestClassifier (bootstrap=True, 200 trees)"
    )

# ── Run ────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
