pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Run Calculator Script') {
            steps {
                sh 'python3 main.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t calculator-app:latest .'
            }
        }

        stage('Push Docker Image') {
            environment {
                DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
            }
            steps {
                script {
                    sh '''
                    echo "$DOCKER_HUB_CREDENTIALS_PSW" | docker login -u "$DOCKER_HUB_CREDENTIALS_USR" --password-stdin
                    docker push ${DOCKER_IMAGE}:${APP_VERSION}
                    docker push ${DOCKER_IMAGE}:latest
                    docker logout
                    '''
                }
            }
        }
    }
}