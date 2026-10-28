import os
import time
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus Metrics Definitions
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP Request Latency in seconds', ['endpoint']
)
PREDICTION_COUNT = Counter(
    'model_predictions_total', 'Total Model Predictions', ['risk_category']
)

# Load Trained Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "heart_disease_model.joblib")
model_bundle = None

def get_model():
    global model_bundle
    if model_bundle is None:
        if os.path.exists(MODEL_PATH):
            model_bundle = joblib.load(MODEL_PATH)
        else:
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run train.py first.")
    return model_bundle

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def track_metrics(response):
    if hasattr(request, 'start_time'):
        latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_result = None
    input_values = {}
    
    if request.method == "POST":
        try:
            bundle = get_model()
            model = bundle["model"]
            features = bundle["features"]
            
            # Extract form values
            input_values = {
                'age': float(request.form.get('age', 55)),
                'sex': int(request.form.get('sex', 1)),
                'cp': int(request.form.get('cp', 0)),
                'trestbps': float(request.form.get('trestbps', 130)),
                'chol': float(request.form.get('chol', 240)),
                'fbs': int(request.form.get('fbs', 0)),
                'restecg': int(request.form.get('restecg', 0)),
                'thalach': float(request.form.get('thalach', 150)),
                'exang': int(request.form.get('exang', 0)),
                'oldpeak': float(request.form.get('oldpeak', 1.0))
            }
            
            df_input = pd.DataFrame([input_values])[features]
            pred_class = int(model.predict(df_input)[0])
            pred_prob = float(model.predict_proba(df_input)[0][1])
            
            label = "High Risk (Heart Disease Indicated)" if pred_class == 1 else "Low Risk (Healthy / Normal)"
            PREDICTION_COUNT.labels(risk_category="High Risk" if pred_class == 1 else "Low Risk").inc()
            
            prediction_result = {
                "class": pred_class,
                "label": label,
                "probability": round(pred_prob * 100, 2),
                "is_high_risk": pred_class == 1
            }
        except Exception as e:
            prediction_result = {
                "error": str(e)
            }
            
    return render_template("index.html", prediction=prediction_result, form_data=input_values)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        bundle = get_model()
        model = bundle["model"]
        features = bundle["features"]
        
        # Verify required features
        for f in features:
            if f not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required feature: '{f}'"
                }), 400
                
        df_input = pd.DataFrame([data])[features]
        pred_class = int(model.predict(df_input)[0])
        pred_proba = float(model.predict_proba(df_input)[0][1])
        risk_label = "High Risk" if pred_class == 1 else "Low Risk"
        
        PREDICTION_COUNT.labels(risk_category=risk_label).inc()
        
        return jsonify({
            "status": "success",
            "prediction": risk_label,
            "class": pred_class,
            "heart_disease_risk_score": round(pred_proba, 4),
            "probability_percentage": round(pred_proba * 100, 2)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health():
    try:
        bundle = get_model()
        model_loaded = bundle is not None
        return jsonify({
            "status": "healthy",
            "service": "CardioPulse Heart Disease MLOps Service",
            "model_loaded": model_loaded,
            "version": "1.0.0"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route("/metrics", methods=["GET"])
def metrics():
    """Prometheus monitoring metrics endpoint"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

