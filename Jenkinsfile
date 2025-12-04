pipeline {

    agent any

    stages {

        stage('Docker Client Setup') {
            steps {
                echo 'Ensuring Docker client is available...'
                // Install the Docker CLI in the Jenkins container
                // This is needed because the base image does not have the docker executable.
                sh '''
                    # Check if docker is already installed. If not, install it.
                    if ! command -v docker &> /dev/null; then
                        echo "Docker client not found. Installing..."
                        apt-get update
                        apt-get install -y docker.io
                    fi
                '''
            }
        }


        stage('Build & Test') {
            // Now that the Docker client is installed, we can use the Docker agent block
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
            // We can switch back to agent any here as the final curl doesn't need Docker
            agent any
            steps {
                echo 'Tests Passed! Deploying to Render...'
                withCredentials([string(credentialsId: 'RENDER_DEPLOY_HOOK_URL', variable: 'RENDER_DEPLOY_HOOK_URL')]) {
                    sh 'curl -X POST $RENDER_DEPLOY_HOOK_URL'
                }
            }
        }        
    }
}
