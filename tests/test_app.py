import os
import sys
import json
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Verify health endpoint responds with 200 and indicates model is loaded."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['model_loaded'] is True

def test_metrics_endpoint(client):
    """Verify Prometheus metrics endpoint is reachable."""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b"http_requests_total" in response.data

def test_home_page_rendering(client):
    """Verify web UI page renders correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"CardioPulse" in response.data

def test_predict_api_valid_high_risk(client):
    """Verify ML inference API with high risk clinical parameters."""
    sample_payload = {
        "age": 65,
        "sex": 1,
        "cp": 0,
        "trestbps": 160,
        "chol": 290,
        "fbs": 1,
        "restecg": 2,
        "thalach": 105,
        "exang": 1,
        "oldpeak": 3.0
    }
    response = client.post('/predict',
                           data=json.dumps(sample_payload),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['class'] in [0, 1]
    assert 'heart_disease_risk_score' in data
    assert 'prediction' in data

def test_predict_api_valid_low_risk(client):
    """Verify ML inference API with healthy/low risk parameters."""
    sample_payload = {
        "age": 35,
        "sex": 0,
        "cp": 2,
        "trestbps": 115,
        "chol": 180,
        "fbs": 0,
        "restecg": 0,
        "thalach": 175,
        "exang": 0,
        "oldpeak": 0.1
    }
    response = client.post('/predict',
                           data=json.dumps(sample_payload),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['class'] == 0
    assert data['prediction'] == "Low Risk"

def test_predict_api_missing_feature(client):
    """Verify error handling on invalid or incomplete payload."""
    incomplete_payload = {
        "age": 55,
        "sex": 1
        # missing other mandatory clinical features
    }
    response = client.post('/predict',
                           data=json.dumps(incomplete_payload),
                           content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert "Missing required feature" in data['message']
