pipeline {
    agent any 

    stages {
        stage('Docker Client Setup (Root)') {
            // Run this entire stage inside a temporary container as the ROOT user
            agent {
                docker { 
                    image 'debian:latest' // Use a lean image that includes apt
                    args '-u root' 
                }
            }
            steps {
                echo 'Installing Docker client and dependencies as ROOT...'
                // These commands now run with root privileges and should succeed.
                sh '''
                    apt-get update
                    apt-get install -y docker.io python3 python3-pip
                '''
            }
        }

        stage('Build & Test') {
            // Now the Docker client is installed and accessible.
            // Switch to the isolated Python container for the build/test.
            agent {
                docker { 
                    image 'python:3.9-slim' 
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                echo 'Running Python Build/Test...'
                // pip is already inside python:3.9-slim, but we run the tests in this isolated environment.
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