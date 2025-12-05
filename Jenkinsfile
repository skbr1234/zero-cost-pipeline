pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Using python3 that we installed into the Jenkins container
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Deploy to Render') {
            when {
                branch 'jenkins-demo'  // only auto-deploy from this branch
            }
            steps {
                withCredentials([string(credentialsId: 'RENDER_DEPLOY_HOOK_URL', variable: 'RENDER_DEPLOY_HOOK_URL')]) {
                    sh 'curl -X POST "$RENDER_DEPLOY_HOOK_URL"'
                }
            }
        }
    }
}
