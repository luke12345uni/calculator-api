pipeline {
    agent any

    environment {
        APP_NAME = "calculator-api"
        DOCKER_IMAGE = "luke12345uni/calculator-api"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/luke12345uni/calculator-api.git'
            }
        }

        // stage('Install Dependencies') {
        //     steps {
        //         sh '''

        //          if ! command -v python3 >/dev/null 2>&1; then
        //             echo "Python3 not found, installing..."
        //             apk add --no-cache python3 py3-pip
        //              ln -sf python3 /usr/bin/python || true
        //           fi

        //           pip3 install -r requirements.txt            
        //         '''
        //     }
        // }
        // stage('Install Dependencies') {
        //     steps {
        //         sh '''

        //          if ! command -v python3 >/dev/null 2>&1; then
        //             echo "Python3 not found, installing..."
        //             apk add --no-cache python3 py3-pip
        //              ln -sf python3 /usr/bin/python || true
        //           fi

        //           pip3 install -r requirements.txt            
        //         '''
        //     }
        // }

        stage('Test Calculator API') {
            steps { 

                // run tests, but don't stop the pipeline if they fail 

                // catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') { 

                    sh'pytest' 

                // } 

            } 

        } 

        stage('Export Test Report') {
            steps {
                // run pytest again just to produce XML 

                sh 'pytest --junitxml=report.xml || true' 

                // show results in Jenkins 

                junit 'report.xml' 

                // let us download the xml 

                archiveArtifacts artifacts: 'report.xml', onlyIfSuccessful: false
            }
        }

        stage('Read Version') {
            steps {
                script {
                    env.APP_VERSION = sh(script: "cat VERSION | tr -d '\\n'", returnStdout: true).trim()
                    echo "Releasing version: ${env.APP_VERSION}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                    docker build -t ${DOCKER_IMAGE}:${APP_VERSION} .
                    docker tag ${DOCKER_IMAGE}:${APP_VERSION} ${DOCKER_IMAGE}:latest
                    '''
                }
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

        stage('Tag Release in GitHub') {
            steps {
                script {
                    sh '''
                    git config user.email "jenkins@localhost"
                    git config user.name "Jenkins CI"
                    git tag -a "v${APP_VERSION}" -m "Release ${APP_VERSION}"
                    git push origin "v${APP_VERSION}" || echo "Skipping tag push"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Build completed. Cleaning up workspace..."
            cleanWs()
        }
    }
}