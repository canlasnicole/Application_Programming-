# 🍷 Wine Class Prediction Web Service

ML model web service using `sklearn`'s `load_wine()` dataset.  
Predicts wine class (class_0 / class_1 / class_2) from 3 selected chemical features.

---

## Project Structure

```
wine_project/
├── train_model.py          # Model training & saving
├── main_gradio_mount.py    # 1.1 Single server (FastAPI + Gradio mounted)
├── api.py                  # 1.2 Separate server — FastAPI backend
├── app_gradio.py           # 1.2 Separate server — Gradio client UI
├── model.pkl               # Saved RandomForest model (generated)
├── scaler.pkl              # Saved StandardScaler (generated)
├── selector.pkl            # Saved feature selector (generated)
└── README.md
```

---

## Dataset

- **Source**: `sklearn.datasets.load_wine()`
- **Samples**: 178
- **Classes**: 3 Italian wine cultivars (class_0, class_1, class_2)
- **Original features**: 13 chemical measurements

---

## Feature Selection

Top 3 features selected via **SelectKBest (ANOVA F-score)**:

| Feature | F-score |
|---|---|
| flavanoids | 233.93 |
| proline | 207.92 |
| od280/od315 of diluted wines | 189.97 |

---

## Model

- **Algorithm**: RandomForestClassifier
- **Parameters**: `n_estimators=200`, `bootstrap=True`, `random_state=42`
- **Preprocessing**: StandardScaler
- **Test accuracy**: **88.89%**

---

## Installation

```bash
pip install scikit-learn fastapi uvicorn gradio joblib
```

---

## How to Run

### Step 0 — Train the model (required first)

```bash
py train_model.py
```

Generates `model.pkl`, `scaler.pkl`, `selector.pkl`.

---

### 1.1 Single Server (Gradio mounted on FastAPI)

One terminal, one port.

```bash
py -m uvicorn main_gradio_mount:app --reload --port 8000
```

| URL | Description |
|---|---|
| http://localhost:8000/gradio | Gradio UI |
| http://localhost:8000/docs | Swagger API docs |
| http://localhost:8000/predict | POST endpoint |

---

### 1.2 Separate Server (FastAPI + Gradio independently)

**Terminal 1 — FastAPI backend:**
```bash
py -m uvicorn api:app --reload --port 8000
```

**Terminal 2 — Gradio client:**
```bash
py app_gradio.py
```

| URL | Description |
|---|---|
| http://localhost:8000/docs | Swagger API docs |
| http://localhost:7860 | Gradio UI |

---

## API Usage

### POST `/predict`

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"flavanoids": 3.06, "od_ratio": 3.92, "proline": 1065}'
```

**Response:**
```json
{
  "predicted_class": "class_0",
  "class_index": 0,
  "probabilities": {
    "class_0": 0.91,
    "class_1": 0.07,
    "class_2": 0.02
  },
  "features_used": ["flavanoids", "od280/od315_of_diluted_wines", "proline"]
}
```

---

## Public Sharing (Gradio)

To share the Gradio UI publicly, edit `app_gradio.py`:

```python
demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
```

A public link will be generated:
```
Running on public URL: https://xxxxxx.gradio.live
```

> ⚠️ Link expires after 1 week. Keep the terminal open while sharing.

---

## Dependency Injection (api.py)

`api.py` uses FastAPI's `Depends` pattern for model loading:

```python
class ModelService:
    def __init__(self):
        self.model  = joblib.load("model.pkl")
        self.scaler = joblib.load("scaler.pkl")

def get_model_service() -> ModelService:
    return _model_service

@app.post("/predict")
def predict(data: WineInput, svc: Annotated[ModelService, Depends(get_model_service)]):
    ...
```

---

## Tech Stack

| Component | Library |
|---|---|
| ML model | scikit-learn |
| API server | FastAPI + Uvicorn |
| UI | Gradio |
| Model persistence | joblib |
| Data validation | Pydantic |
