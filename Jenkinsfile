pipeline {
    agent {
        docker {
            image 'python:3.12'
            args '-v /var/jenkins_home:/var/jenkins_home'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh 'pytest'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t calculator-api .'
            }
        }
    }
    post {
        always {
            echo 'Pipeline finished'
        }
    }
}
