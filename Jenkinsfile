pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "Pulling latest code from GitHub..."
                sh 'git clone -b main https://github.com/luke12345uni/calculator-api.git || echo "Repo already cloned"'
                dir('calculator-api') {
                    echo "Changed directory to calculator-api"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh 'pip install --upgrade pip'
                sh 'pip install -r calculator-api/requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "Running unit tests..."
                sh 'pytest --maxfail=1 --disable-warnings -q calculator-api/tests/'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t calculator-api:latest calculator-api'
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully: Build, tests, Docker image done!"
        }
        failure {
            echo "❌ Pipeline failed. Check console output for details."
        }
    }
}
