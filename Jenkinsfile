pipeline {
    agent any

    environment {
        APP_NAME = "cardiopulse-ml-app"
        APP_PORT = "5000"
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('1. Checkout SCM') {
            steps {
                echo 'Checking out source code from Git repository...'
                checkout scm
            }
        }

        stage('2. Tool & Environment Verification') {
            steps {
                echo 'Verifying environment tools on the build node...'
                bat '''
                    python --version
                    pip --version
                    git --version
                    docker --version
                '''
            }
        }

        stage('3. Install Dependencies') {
            steps {
                echo 'Installing required Python libraries...'
                bat '''
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('4. Automated Unit Testing (pytest)') {
            steps {
                echo 'Executing automated unit tests and API contract checks...'
                bat '''
                    python -m pytest -v --junitxml=test-results.xml
                '''
            }
        }

        stage('5. Docker Image Build') {
            steps {
                echo 'Building Docker container image for CardioPulse...'
                bat '''
                    docker build -t %APP_NAME%:latest -t %APP_NAME%:%BUILD_NUMBER% .
                '''
            }
        }

        stage('6. Deploy & Health Check') {
            steps {
                echo 'Running container and verifying service health...'
                bat '''
                    docker stop %APP_NAME% || exit 0
                    docker rm %APP_NAME% || exit 0
                    docker run -d --name %APP_NAME% -p %APP_PORT%:%APP_PORT% %APP_NAME%:latest
                    timeout /t 5 /nobreak
                    curl -s http://localhost:%APP_PORT%/health
                '''
            }
        }

        stage('7. Monitoring Verification') {
            steps {
                echo 'Probing Prometheus metrics and telemetry endpoint...'
                bat '''
                    curl -s http://localhost:%APP_PORT%/metrics
                '''
            }
        }
    }

    post {
        always {
            echo 'Archiving test results and cleaning up...'
            junit allowEmptyResults: true, testResults: 'test-results.xml'
        }
        success {
            echo "CI/CD Pipeline executed successfully! CardioPulse is ready for production."
        }
        failure {
            echo "Pipeline failed. Review stage logs for diagnosis."
        }
    }
}
