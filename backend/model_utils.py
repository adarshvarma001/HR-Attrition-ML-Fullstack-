import os
import joblib
import pandas as pd
from typing import Dict, Any

MODEL_PATH = os.environ.get("MODEL_PATH", "BEST_Attrition_Ensemble.joblib")

_model = None
_model_meta = None

def load_model(path: str = MODEL_PATH):
    global _model, _model_meta
    if _model is None:
        _model = joblib.load(path)
        # Try to extract metadata (best-effort)
        _model_meta = {}
        try:
            # If model is a Pipeline or VotingClassifier with named_estimators_
            if hasattr(_model, "named_estimators_"):
                est = list(_model.named_estimators_.values())[0]
                if hasattr(est, "named_steps"):
                    for step in est.named_steps.values():
                        if hasattr(step, "transformers_"):
                            for name, transformer, cols in step.transformers_:
                                try:
                                    if transformer.__class__.__name__ == "OneHotEncoder":
                                        _model_meta["ohe_cols"] = cols
                                        _model_meta["ohe_categories"] = [list(c) for c in transformer.categories_]
                                    elif hasattr(transformer, "named_steps"):
                                        for sub in transformer.named_steps.values():
                                            if sub.__class__.__name__ == "OneHotEncoder":
                                                _model_meta["ohe_cols"] = cols
                                                _model_meta["ohe_categories"] = [list(c) for c in sub.categories_]
                                except Exception:
                                    continue
        except Exception:
            _model_meta = _model_meta or {}
    return _model

def predict_from_dict(input_dict: Dict[str, Any]):
    model = load_model()
    df = pd.DataFrame([input_dict])
    proba = model.predict_proba(df)[:,1][0]
    label = "Yes" if proba >= 0.5 else "No"
    return float(proba), label

def get_model_meta():
    load_model()
    return _model_meta or {}
