pipeline {
    agent {
        docker {
            image 'python:3.12'
            args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Pulling latest code from GitHub..."
                git 'https://github.com/luke12345uni/calculator-api.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "Running unit tests..."
                sh 'pytest --maxfail=1 --disable-warnings -q tests/'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t calculator-api:latest .'
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs for details."
        }
    }
}
