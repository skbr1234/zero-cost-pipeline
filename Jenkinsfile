pipeline {
    // Default agent for stages that don't need special privileges
    agent any 

    stages {
        stage('Docker Client Setup (Root)') {
            // Temporarily run this stage as the root user to install packages
            agent {
                label 'master' // Use the built-in Jenkins executor
                // Execute commands as root user
                args '-u root' 
            }
            steps {
                echo 'Ensuring Docker client is available (Running as root)...'
                sh '''
                    # Install Docker client and clean up
                    apt-get update
                    apt-get install -y docker.io
                    apt-get clean
                '''
            }
        }

        stage('Build & Test') {
            // Now that Docker is installed, switch to the isolated Python container
            agent {
                docker { 
                    image 'python:3.9-slim' 
                    // Tell the Python container to use the shared Docker socket
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                echo 'Installing Python Dependencies...'
                sh 'pip install -r requirements.txt' 
                echo 'Running Tests...'
                sh 'pytest'
            }
        }
        
        stage('Deploy') {
            agent any // Use the built-in Jenkins executor for the final curl command
            steps {
                echo 'Tests Passed! Deploying to Render...'
                withCredentials([string(credentialsId: 'RENDER_DEPLOY_HOOK_URL', variable: 'RENDER_DEPLOY_HOOK_URL')]) {
                    sh 'curl -X POST $RENDER_DEPLOY_HOOK_URL'
                }
            }
        }
    }
}