"""
train_model.py
─────────────────────────────────────────────
- Dataset   : sklearn load_wine()
- Feature   : SelectKBest(f_classif, k=3)
              → flavanoids, od280/od315_of_diluted_wines, proline
- Model     : RandomForestClassifier (bootstrap=True)
- Output    : model.pkl, scaler.pkl, selector.pkl
"""

import numpy as np
import joblib
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# ── 1. Load data ───────────────────────────────────
wine       = load_wine()
X_all, y   = wine.data, wine.target
CLASS_NAMES = wine.target_names.tolist()   # ['class_0','class_1','class_2']

# ── 2. Feature selection (top 3) ───────────────────
selector   = SelectKBest(f_classif, k=3)
X_sel      = selector.fit_transform(X_all, y)

mask            = selector.get_support()
SELECTED_FEATS  = [wine.feature_names[i] for i, m in enumerate(mask) if m]
# → ['flavanoids', 'od280/od315_of_diluted_wines', 'proline']

# ── 3. Train / test split ──────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_sel, y, test_size=0.2, random_state=42
)

# ── 4. Scaling ─────────────────────────────────────
scaler      = StandardScaler()
X_train_sc  = scaler.fit_transform(X_train)
X_test_sc   = scaler.transform(X_test)

# ── 5. Model (RandomForest with bootstrap) ─────────
model = RandomForestClassifier(
    n_estimators=200,
    bootstrap=True,          # ← 교수님 요구사항
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train_sc, y_train)

# ── 6. Evaluate ────────────────────────────────────
y_pred   = model.predict(X_test_sc)
accuracy = accuracy_score(y_test, y_pred)
report   = classification_report(y_test, y_pred, target_names=CLASS_NAMES)

print("=" * 50)
print("  ✅  Wine Model Training Complete")
print("=" * 50)
print(f"  Selected features : {SELECTED_FEATS}")
print(f"  Test accuracy     : {accuracy*100:.2f}%")
print("─" * 50)
print(report)

# ── 7. Save artifacts ──────────────────────────────
joblib.dump(model,    "model.pkl")
joblib.dump(scaler,   "scaler.pkl")
joblib.dump(selector, "selector.pkl")
print("  💾  Saved: model.pkl / scaler.pkl / selector.pkl")
print("=" * 50)

# ── Helper: feature ranges (for UI sliders) ────────
FEATURE_RANGES = {
    feat: (float(X_sel[:, i].min()), float(X_sel[:, i].max()))
    for i, feat in enumerate(SELECTED_FEATS)
}

if __name__ == "__main__":
    pass   # run this file directly: python train_model.py
