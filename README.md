# 🚀 Zero-Cost CI/CD with Jenkins & Render
### (Jenkins Demo Branch)

This branch demonstrates how to implement a **cost-efficient CI/CD pipeline** for a Python application using:

- **Jenkins** as the CI/CD orchestrator  
- **Render** as the deployment platform  
- A **local Jenkins runner** to avoid paid infrastructure or cloud-hosted CI servers  

The primary objective is to showcase an **enterprise-style CI/CD setup** without requiring paid compute resources such as GitHub self-hosted runners, AWS EC2 build nodes, or managed CI infrastructure.

> This `jenkins-demo` branch is referenced from a LinkedIn post and contains the Jenkins-based implementation.  
> The `main` branch contains the GitHub Actions version.

---

## 🔧 High-Level Architecture

```
GitHub (jenkins-demo branch)
        │
        ▼
Jenkins Pipeline
(runs locally to reduce infra cost)
        │
        ▼
Build + Test (PyTest)
        │
        ▼
Render Deployment (Deploy Hook)
```

![Jenkins CI/CD Architecture](./docs/jenkins-architecture.svg)

---

## 📁 Project Structure (this branch)

```
├── Jenkinsfile          # Jenkins pipeline configuration
├── app.py               # Python application
├── requirements.txt     # Python dependencies
├── test_app.py          # Unit test executed in CI
└── README.md            # Documentation for Jenkins pipeline
```

> `.github/workflows` used by GitHub Actions is intentionally removed in this branch — CI/CD here uses Jenkins exclusively.

---

## 🧪 Pipeline Capabilities

| Stage | Responsibility |
|--------|----------------|
| Checkout | Pull latest code from GitHub |
| Install Dependencies | Create virtual environment & install packages |
| Run Tests | Execute PyTest suite |
| Deploy to Render | Trigger deployment via secure deploy hook |

---

## 🛠 Prerequisites

Before running the pipeline:

- Docker installed locally
- Render Web Service already created for this repository
  - Auto-deploy disabled
  - Deploy Hook URL available in ⚙️ Settings → Deploy Hooks
- Basic familiarity with Jenkins UI

---

## 1️⃣ Run Jenkins in Docker

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  --restart=on-failure \
  -v jenkins_home:/var/jenkins_home \
  --user root \
  jenkins/jenkins:lts-jdk17
```

- Jenkins UI → `http://localhost:8080`
- Running as `root` enables installation of build tools without permission issues

---

## 2️⃣ Install Python Build Tools inside Jenkins Container

```bash
docker exec -it -u 0 jenkins bash

apt-get update
apt-get install -y python3 python3-venv python3-pip

exit
```

This enables Jenkins to create Python virtual environments and install dependencies during the build pipeline.

---

## 3️⃣ Configure Deployment Secret in Jenkins

In Jenkins UI:

```
Manage Jenkins → Credentials → Global → Add Credentials
```

| Field | Value |
|--------|--------|
| Kind | Secret Text |
| ID | `RENDER_DEPLOY_HOOK_URL` |
| Secret | Render deploy hook URL |

---

## 4️⃣ Create a Pipeline Job in Jenkins

**New Item → Pipeline → Pipeline script from SCM**

| Field | Value |
|--------|--------|
| SCM | Git |
| Repository URL | `https://github.com/skbr1234/zero-cost-pipeline` |
| Branch | `jenkins-demo` |
| Lightweight Checkout | Disable |

---

## 5️⃣ Jenkinsfile (already included in this branch)

```groovy
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
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/pytest'
            }
        }

        stage('Deploy to Render') {
            steps {
                withCredentials([string(credentialsId: 'RENDER_DEPLOY_HOOK_URL', variable: 'RENDER_DEPLOY_HOOK_URL')]) {
                    sh 'curl -X POST "$RENDER_DEPLOY_HOOK_URL"'
                }
            }
        }
    }
}
```

---

## 🧠 Troubleshooting Guidance

| Issue | Fix |
|--------|------|
| `externally-managed-environment` error | Ensure `python3-venv` is installed |
| Git checkout fails | Disable Lightweight checkout + verify branch |
| Deploy skipped | Check Render secret + build success |

---

## 🚀 Enhancement Ideas (Future Work)

- Add linting (`flake8`, `black`)
- Add Docker image build stage
- Deploy containerized workloads
- Add Slack/email failure notifications

---

## 🏁 Summary

This demo illustrates how to:

- Build a reliable CI/CD pipeline for Python applications
- Deploy to Render using secure deploy hooks
- Avoid CI infrastructure cost by running Jenkins locally
- Maintain separation between GitHub Actions and Jenkins implementations
