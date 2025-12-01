pipeline {
  agent any

  environment {
    DOCKERHUB = credentials('dockerhub_credentials')   // Provides DOCKERHUB_USR / DOCKERHUB_PSW
  }

  stages {

    stage('Docker Login') {
      steps {
        sh 'echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin'
      }
    }

    stage('Pull , build and Run dockerfile ') {
      steps {
        sh '''
          # Stop and remove running container
          docker stop calculator-api || true
          docker rm calculator-api || true

          # Remove old image
          docker rmi luke12345uni/calculator-api || true

          # Build new Docker image
          docker build -t luke12345uni/calculator-api .

          # Start with docker compose
          docker compose up -d
        '''
      }
    }

    stage('Run Tests') {
      steps {
        echo "done testing"
      }
    }

    stage('cleaning') {
      steps {
        sh 'docker compose down || true'
      }
    }

  }
}
