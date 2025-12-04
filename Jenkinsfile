pipeline {

    // 1. Tell Jenkins to run all subsequent stages inside this Python image
    agent {
        docker { 
            image 'python:3.9-slim' 
        }
    }

    stages {
        stage('Setup') {
            steps {
                echo 'Installing Python Dependencies...'
                // Python and pip are already available thanks to the Docker agent
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
