import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def generate_heart_data(n_samples=1000, random_state=42):
    """
    Generates realistic clinical dataset modeled after the Cleveland Heart Disease dataset.
    Features:
      - age: age in years
      - sex: 1 = male, 0 = female
      - cp: chest pain type (0: typical angina, 1: atypical angina, 2: non-anginal pain, 3: asymptomatic)
      - trestbps: resting blood pressure in mm Hg (90 - 200)
      - chol: serum cholesterol in mg/dl (120 - 400)
      - fbs: fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
      - restecg: resting electrocardiographic results (0, 1, 2)
      - thalach: maximum heart rate achieved (70 - 210)
      - exang: exercise induced angina (1 = yes; 0 = no)
      - oldpeak: ST depression induced by exercise relative to rest (0.0 - 5.0)
    """
    np.random.seed(random_state)
    
    age = np.random.randint(28, 78, size=n_samples)
    sex = np.random.choice([0, 1], size=n_samples, p=[0.45, 0.55])
    cp = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.48, 0.17, 0.28, 0.07])
    trestbps = np.random.normal(130, 17, size=n_samples).clip(94, 200).astype(int)
    chol = np.random.normal(245, 50, size=n_samples).clip(126, 450).astype(int)
    fbs = (np.random.rand(n_samples) < 0.15).astype(int)
    restecg = np.random.choice([0, 1, 2], size=n_samples, p=[0.5, 0.48, 0.02])
    thalach = np.random.normal(150, 25, size=n_samples).clip(71, 202).astype(int)
    exang = np.random.choice([0, 1], size=n_samples, p=[0.68, 0.32])
    oldpeak = np.random.exponential(0.8, size=n_samples).clip(0.0, 5.0).round(1)
    
    # Clinical risk score calculation for realistic correlation
    risk_score = (
        0.04 * (age - 50) +
        0.6 * sex +
        0.5 * (3 - cp) +
        0.015 * (trestbps - 120) +
        0.008 * (chol - 200) +
        0.4 * fbs +
        0.3 * restecg -
        0.025 * (thalach - 140) +
        0.8 * exang +
        0.5 * oldpeak +
        np.random.normal(0, 0.5, size=n_samples)
    )
    
    target = (risk_score > np.percentile(risk_score, 52)).astype(int)
    
    df = pd.DataFrame({
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg,
        'thalach': thalach,
        'exang': exang,
        'oldpeak': oldpeak,
        'target': target
    })
    return df

def train_and_save_model(model_dir="model"):
    os.makedirs(model_dir, exist_ok=True)
    df = generate_heart_data()
    
    X = df.drop(columns=['target'])
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Training Complete!")
    print(f"Validation Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    model_data = {
        "model": model,
        "features": list(X.columns),
        "target_names": ["Low Risk (Healthy)", "High Risk (Heart Disease)"]
    }
    
    model_path = os.path.join(model_dir, "heart_disease_model.joblib")
    joblib.dump(model_data, model_path)
    print(f"Model artifact successfully saved to: {model_path}")

if __name__ == "__main__":
    train_and_save_model()

