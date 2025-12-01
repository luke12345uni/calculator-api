pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-u root'
        }
    }

    stages {

        stage('Run script') {
            steps {
                sh 'python3 main.py'
            }
        }

        stage('Test Calculator API') {
            steps {
                sh 'pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t luke12345uni/calculator-api .'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin
                    docker push luke12345uni/calculator-api
                '''
            }
        }
    }
}
