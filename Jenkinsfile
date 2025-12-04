pipeline {
    // 1. Define a generic agent globally (used by Setup and Deploy)
    agent any 

    stages {
        stage('Docker Client Setup (Root)') {
            // This stage uses the top-level 'agent any' (the Jenkins master node).
            // The logic is moved into a 'script' block to bypass syntax limitations.
            steps {
                echo 'Ensuring Docker client is available (Attempting root install)...'
                
                // *** Use a 'script' block for privileged commands ***
                script {
                    // We attempt to run the privileged commands with sudo first, 
                    // and then without (||) to handle Docker environment variances.
                    sh 'sudo apt-get update || apt-get update' 
                    sh 'sudo apt-get install -y docker.io || apt-get install -y docker.io' 
                }
            }
        }

        stage('Build & Test') {
            // 2. Override the global agent to run inside the Python Docker container
            agent {
                docker { 
                    image 'python:3.9-slim' 
                    // Mount the host Docker socket for the Docker-in-Docker functionality
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
            agent any // Falls back to the global agent for the final secure curl command
            steps {
                echo 'Tests Passed! Deploying to Render...'
                // Using the consistent RENDER_DEPLOY_HOOK_URL for security
                withCredentials([string(credentialsId: 'RENDER_DEPLOY_HOOK_URL', variable: 'RENDER_DEPLOY_HOOK_URL')]) {
                    sh 'curl -X POST $RENDER_DEPLOY_HOOK_URL'
                }
            }
        }
    }
}