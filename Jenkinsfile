pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Installing Dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running Tests...'
                sh 'pytest'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Tests Passed! Deploying to Render...'
                // 'withCredentials' injects the secret into this specific step securely
                withCredentials([string(credentialsId: 'RENDER_DEPLOY_HOOK_URL', variable: 'DEPLOY_URL')]) {
                    // We use the $DEPLOY_URL variable effectively masking the real URL
                    sh 'curl -X POST $RENDER_DEPLOY_HOOK_URL'
                }
            }
        }
    }
}
