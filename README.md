# 🚀 Zero-Cost CI/CD Pipeline Demo

![Build Status](https://github.com/skbr1234/zero-cost-pipeline/actions/workflows/pipeline.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📖 Overview
This project demonstrates a production-grade **Continuous Integration and Continuous Deployment (CI/CD)** pipeline built entirely with free tools.

The goal was to create a "GitOps" workflow where code changes are automatically tested and, upon passing, deployed to a live server without manual intervention.

**Live Demo:** [https://zero-cost-pipeline.onrender.com/]

---

## ⚙️ Architecture

The pipeline follows a strict logic: **"Code is only deployed if it passes tests."**

```mermaid
graph LR
    A[Developer] -->|Push Code| B(GitHub Repo)
    B -->|Trigger| C{GitHub Actions CI}
    C -->|Run Tests| D[Pytest]
    D -->|Pass| E[Trigger Webhook]
    D -->|Fail| F[Stop Pipeline 🛑]
    E -->|Deploy| G[Render Cloud]
    G -->|Live| H[Production App]
