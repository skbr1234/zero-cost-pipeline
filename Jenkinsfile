pipeline {
    agent any

    options {
        cleanWs()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                // Either run tests directly in the container…
                sh '''
                    pip install -r requirements.txt
                    pytest
                '''

                // …or use Docker (since you have the host Docker socket)
                // docker build -t my-flask-app:test .
                // docker run --rm my-flask-app:test pytest
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'RENDER_DEPLOY_HOOK_URL', variable: 'RENDER_DEPLOY_HOOK_URL')]) {
                    sh 'curl -X POST "$RENDER_DEPLOY_HOOK_URL"'
                }
            }
        }
    }
}
