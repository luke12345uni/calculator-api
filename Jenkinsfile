pipeline {
    agent any

    environment {
        IMAGE_NAME = 'luke1567/main'
        DOCKERHUB = credentials('dockerhub-credentials')
    }

    stages {
        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Run Calculator Script') {
            steps {
                sh 'python3 app/main.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t calculator-app:latest .'
            }
        }

        stage('Push Docker Image') {
            steps {
                
                    sh ''' 
                      docker push ${IMAGE_NAME}:latest
                    '''
                
            }
        }
    }
}