# CICD pipeline and Monitoring Tools
## Summary Report

### Student Details
| Details | Student Entry |
| :--- | :--- |
| **Student Name** | *[Enter Your Name]* |
| **Roll Number(s)** | *[Enter Your Roll Number]* |
| **Department / Class** | Final Year B. Tech - CSE (Artificial Intelligence and Machine Learning) Sem - VII |
| **Academic Year** | A.Y 2026-27 |
| **GitHub Repository URL** | *[Enter Your GitHub Repository URL]* |

---

## 1. Problem Statement

Develop an end-to-end Machine Learning Web Application for **Heart Disease Risk Prediction (CardioPulse)** and implement the complete DevOps / MLOps lifecycle on a Windows PC. The project utilizes **Scikit-Learn** for training an accurate clinical risk classification model and **Flask** for serving both an interactive web dashboard and a REST API. **Git** is employed for local version control, **GitHub** for cloud source-code hosting, **Docker** for application containerization, and **Jenkins** for automating the continuous integration and deployment pipeline (including automated pytest test suites and container image builds). In addition, **Prometheus monitoring** and health-check endpoints are incorporated to capture real-time latency, request rates, and prediction distribution metrics. Each tool is installed, configured, verified, and orchestrated using Windows commands to ensure a seamless transition from development to production.

---

## 2. Tools: Environment Setup

### 1. Python and Flask — Web Application & Machine Learning Development
#### 1. Environment Setup
- Install Python 3.13 and configure the system PATH environment variable.
- Install Flask, Scikit-Learn, Pandas, Joblib, Prometheus Client, and Pytest.
- Train and validate the Heart Disease Random Forest model via `train.py`, generating `model/heart_disease_model.joblib`.
- Verify installed versions and launch the Flask web application.

#### 2. Commands to Run on Windows
- `python --version`
- `pip --version`
- `pip install -r requirements.txt`
- `python train.py`
- `python -m pytest -v`
- `python app.py`

---

### 2. Git — Version Control
#### 1. Environment Setup
- Install Git for Windows and verify CLI availability.
- Configure the Git username and user email globally.
- Initialize local git repository and stage all MLOps application files.

#### 2. Commands to Run on Windows
- `git --version`
- `git init`
- `git status`
- `git add .`
- `git commit -m "Initial commit: CardioPulse ML App with CI/CD & Monitoring"`

---

### 3. GitHub — Source-Code Hosting
#### 1. Environment Setup
- Create a GitHub account and a remote repository for the project.
- Configure Git authentication using Git Credential Manager or Personal Access Token (PAT).
- Set the default branch to main and push local commits to the remote origin.

#### 2. Commands to Run on Windows
*(Replace `REPOSITORY_URL` with the actual URL of your GitHub repository)*
- `git remote add origin REPOSITORY_URL`
- `git branch -M main`
- `git push -u origin main`
- `git pull origin main`

---

### 4. Docker — Application Containerization
#### 1. Environment Setup
- Install Docker Desktop on Windows and configure WSL 2 backend.
- Verify Docker Engine daemon and Docker Compose availability.
- Build the container image using the Dockerfile and launch the container on port 5000.

#### 2. Commands to Run on Windows
- `docker --version`
- `docker compose version`
- `docker info`
- `docker build -t cardiopulse-ml-app .`
- `docker run -d -p 5000:5000 --name cardiopulse-service cardiopulse-ml-app`
- `docker ps`

---

### 5. Jenkins — Continuous Integration and Continuous Deployment
#### 1. Environment Setup
- Verify Java JDK 23 compatibility with Jenkins.
- Install and configure Jenkins, and verify the Java and Jenkins versions.
- Configure Jenkins Declarative Pipeline job linked to the GitHub repository and execute `Jenkinsfile`.

#### 2. Commands to Run on Windows
**For Jenkins installed directly on Windows:**
- `java -version`
- `git --version`
- `docker --version`
- `jenkins.exe start` *(only if using a Jenkins installation that provides this service command)*

**For Jenkins running as a Docker container named jenkins:**
- `docker run -d -p 8080:8080 -p 50000:50000 --name jenkins jenkins/jenkins:lts`
- `docker ps`
- `docker logs jenkins`
- `docker exec jenkins java -version`

---

### 6. Monitoring Tools — Prometheus & Health Telemetry
#### 1. Environment Setup
- Integrate `prometheus-client` into Flask application to collect real-time HTTP metrics and model inference counters.
- Configure health probe endpoint (`/health`) for container liveness and readiness verification.
- Expose Prometheus telemetry endpoint (`/metrics`) to track latency, request counts, and prediction drift.

#### 2. Commands to Run on Windows
- `curl -s http://localhost:5000/health`
- `curl -s http://localhost:5000/metrics`
- `curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"age\":55,\"sex\":1,\"cp\":0,\"trestbps\":140,\"chol\":250,\"fbs\":0,\"restecg\":1,\"thalach\":140,\"exang\":1,\"oldpeak\":2.0}"`
