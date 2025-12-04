pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Installing Python and Dependencies...'
                // Running these commands with elevated privileges (sudo/root)
                sh """
                    apt-get update && \
                    apt-get install -y python3 python3-pip
                """
                // Note: The 'pip' command below runs as the 'jenkins' user but now works because Python is installed
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
