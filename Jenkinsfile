pipeline {
    agent {
        docker {
            image 'python:3.12'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    environment {
        APP_DIR = 'app'
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/luke12345uni/calculator-api.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running tests...'
                sh 'pytest tests --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t calculator-api:latest .'
            }
        }
    }
    post {
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed. Check console output for details.'
        }
    }
}
