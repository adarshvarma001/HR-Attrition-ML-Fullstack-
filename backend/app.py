# backend/app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from model_utils import predict_from_dict, get_model_meta, load_model
from suggestions import suggestions_for_row
import os

app = Flask(__name__, static_folder=None)  # static_folder set for production build option later
CORS(app, resources={r"/*": {"origins": "*"}})

FEATURES = [
    'Age', 'MonthlyIncome', 'JobRole', 'TotalWorkingYears', 'WorkLifeBalance',
    'DistanceFromHome', 'YearsSinceLastPromotion', 'PerformanceRating', 'OverTime'
]

# --------------------------------------
# Load model once at startup (Flask 3.x safe)
# --------------------------------------
print("🔄 Loading model at startup...")
try:
    load_model()
    print("✅ Model loaded successfully")
except Exception as e:
    # log but allow the app to start — prediction endpoint will return an error if model missing
    print("❌ Model failed to load at startup:", e)

# --------------------------------------
# Routes
# --------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/meta", methods=["GET"])
def meta():
    meta = get_model_meta()
    return jsonify({"features": FEATURES, "meta": meta})

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)

    # check required features
    missing = [f for f in FEATURES if f not in payload]
    if missing:
        return jsonify({"error": f"Missing features: {missing}"}), 400

    # convert numeric types (best-effort)
    numeric_keys = [
        'Age','MonthlyIncome','TotalWorkingYears','WorkLifeBalance',
        'DistanceFromHome','YearsSinceLastPromotion','PerformanceRating'
    ]
    for k in numeric_keys:
        if k in payload:
            try:
                payload[k] = int(payload[k])
            except Exception:
                # leave original if conversion fails
                pass

    # run prediction
    try:
        proba, label = predict_from_dict(payload)
    except Exception as e:
        # include helpful debugging message while developing
        return jsonify({"error": f"Model prediction error: {str(e)}"}), 500

    suggestions = suggestions_for_row(payload)
    return jsonify({
        "attrition_probability": round(proba, 4),
        "attrition_label": label,
        "suggestions": suggestions
    })

# --- optional: serve built frontend in production
# Put built React files in backend/static_build (or change path)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    build_folder = os.environ.get("FRONTEND_BUILD_PATH", None)
    if build_folder and os.path.exists(os.path.join(build_folder, path or "index.html")):
        if path != "" and os.path.exists(os.path.join(build_folder, path)):
            return send_from_directory(build_folder, path)
        else:
            return send_from_directory(build_folder, "index.html")
    return jsonify({"status":"backend running"}), 200

if __name__ == "__main__":
    # convenient dev run
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
