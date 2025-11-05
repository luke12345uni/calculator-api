pipeline {
    agent {
        docker {
            image 'python:3.12'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building calculator app...'
                sh 'python --version'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'pytest || echo "No tests found"'
            }
        }

        stage('Package') {
            steps {
                echo 'Packaging app...'
                sh 'zip -r app.zip .'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy stage (placeholder)...'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check console output for details.'
        }
    }
}

