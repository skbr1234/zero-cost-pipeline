pipeline {
    // Define a generic agent globally
    agent any 

    options {
        cleanWs() 
    }

    stages {
        stage('Install Docker Client') {
            // This stage uses 'agent any' (the Jenkins master node).
            // We use 'script' to handle the installation and permission gymnastics.
            steps {
                echo 'Attempting to install Docker client on Jenkins executor...'
                
                script {
                    // This command uses the standard apt-get repository to install the Docker client
                    // and relies on the persistent volume/socket mount to work.
                    // We run these commands using a simplified shell execution.
                    sh '''
                        # Install necessary tools if not present
                        apt-get update
                        apt-get install -y docker.io
                        # Add the Jenkins user to the docker group (often required for DooD)
                        usermod -aG docker jenkins
                    '''
                }
            }
        }

        stage('Build & Test') {
            // Now the Docker client is installed and the user is in the docker group.
            agent {
                docker { 
                    image 'python:3.9-slim' 
                    // This argument tells the inner container to use the host's Docker socket
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                echo 'Running Python Build/Test in isolated container...'
                sh 'pip install -r requirements.txt' 
                sh 'pytest'
            }
        }
        
        stage('Deploy') {
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