pipeline {

    /******************************
     * Global Settings
     ******************************/
    agent any

    environment {
        APP_NAME      = "calculator-api"
        DOCKER_IMAGE  = "luke12345uni/calculator-api"
    }

    stages {

        /******************************
         * CHECKOUT SOURCE CODE
         ******************************/
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/luke12345uni/calculator-api.git'
            }
        }


        /******************************
         * RUN TESTS INSIDE PYTHON DOCKER IMAGE
         ******************************/
        stage('Test Calculator API') {
            agent {
                docker {
                    image 'python3'
                }
            }
            steps {
                sh '''
                    pip install -r requirements.txt
                    pytest
                '''
            }
        }


        /******************************
         * GENERATE TEST REPORT
         ******************************/
        stage('Export Test Report') {
            agent {
                docker {
                    image 'python3'
                }
            }
            steps {
                sh '''
                    pip install -r requirements.txt
                    pytest --junitxml=report.xml || true
                '''
                junit 'report.xml'
                archiveArtifacts artifacts: 'report.xml', onlyIfSuccessful: false
            }
        }


        /******************************
         * READ VERSION FROM VERSION FILE
         ******************************/
        stage('Read Version') {
            steps {
                script {
                    env.APP_VERSION = sh(script: "cat VERSION | tr -d '\\n'", returnStdout: true).trim()
                    echo "Releasing version: ${env.APP_VERSION}"
                }
            }
        }


        /******************************
         * BUILD DOCKER IMAGE
         ******************************/
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${APP_VERSION} .
                    docker tag ${DOCKER_IMAGE}:${APP_VERSION} ${DOCKER_IMAGE}:latest
                '''
            }
        }


        /******************************
         * PUSH DOCKER IMAGE TO DOCKER HUB
         ******************************/
        stage('Push Docker Image') {
            environment {
                DOCKER_HUB = credentials('dockerhub-credentials')
            }
            steps {
                sh '''
                    echo "$DOCKER_HUB_PSW" | docker login -u "$DOCKER_HUB_USR" --password-stdin
                    docker push ${DOCKER_IMAGE}:${APP_VERSION}
                    docker push ${DOCKER_IMAGE}:latest
                    docker logout || true
                '''
            }
        }


        /******************************
         * TAG RELEASE IN GITHUB
         ******************************/
        stage('Tag Release in GitHub') {
            steps {
                sh '''
                    git config user.email "jenkins@localhost"
                    git config user.name "Jenkins CI"

                    git tag -a "v${APP_VERSION}" -m "Release ${APP_VERSION}"
                    git push origin "v${APP_VERSION}" || echo "Tag already exists or push skipped"
                '''
            }
        }
    }


    /******************************
     * ALWAYS CLEAN WORKSPACE
     ******************************/
    post {
        always {
            echo "Build completed. Cleaning up workspace..."
            cleanWs()
        }
    }

}
