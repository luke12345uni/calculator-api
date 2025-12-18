pipeline {
    agent any

    environment {
        IMAGE_NAME = 'luke1567/calc9'
        DOCKERHUB = credentials('dockerhub-credentials')
    }

    stages {
        stage('Run Tests') {
            steps {
                sh 'pytest'
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

        // stage('Run Calculator Script') {
        //     steps {
        //         sh 'python3 app/main.py'
        //     }
        // }

        // stage('Build Docker Image') {
        //     steps {
        //         sh 'docker build -t calculator-app:latest .'
        //     }
        // }

        stage('Docker Login') {
            steps {
                sh 'echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin'
            }
        }
                stage('Build image') {
            steps {
                sh '''
                docker build \
                    -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                    -t ${IMAGE_NAME}:latest \
                    .
                '''
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
