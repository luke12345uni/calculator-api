pipeline {
    agent {
        docker {
            image 'python:3.12'          // Python and pip already installed
            args '-u root:root'          // run as root for pip installs
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
                // Use host Docker (requires Docker-in-Docker or socket mount)
                sh 'docker build -t calculator-api:latest . || echo "Docker not available, skipping"'
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
