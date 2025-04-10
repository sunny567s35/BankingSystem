# 🏦 Banking System
**BankingSystem** is a robust, production-ready online banking application built using Django, React, MySQL, and modern DevOps tooling. It simulates core banking operations including account management, transactions, interest calculations, and user authentication. This project integrates modern SRE (Site Reliability Engineering) principles, ensuring high availability, observability, scalability, and operational efficiency.

The application architecture adopts a microservices-inspired modular design, allowing services like account management, transaction processing, interest calculations, and authentication to work independently and communicate seamlessly.
We built the **BankingSystem** project to tackle real-world banking complexity while applying SRE principles like observability, CI/CD, and containerized deployment using Prometheus, Grafana, Celery, Docker, and Kubernetes.

---
Team Contribution:
- Backend - Vishnu, Chaitanya, Sandeep
- Frontend - Sindhuja, Himaansh
- Dockerfile - Hema
- Kubernetes - Khushi, Himaansh
- Jenkins - Sandeep, Vishnu
- Prometheus & Grafana - Sindhuja, Khushi
* * *
# 🏦 BankingSystem Deployment Guide

--- 
## ✅ Prerequisites - DockerHub account (username & password)

---
## 🚀 Ubuntu Instructions 
### 1. Clone the repository 
```bash
git clone https://github.com/KhushiGK/BankingSystem.git
git clone git@github.com:KhushiGK/BankingSystem.git
cd BankingSystem` 
```
### 2\. Set DockerHub image name

Edit the following files:

*   `k8s/deployment.yaml` → `image: <your-dockerhub-username>/banking-system:v1`
    
*   `k8s/react-deployment.yaml` → `image: <your-dockerhub-username>/banking-system:v1`
    

* * *

### 3\. Build, Push, and Deploy (First Time Setup)

`chmod 777 deploy.sh
./deploy.sh` 

This will:
Install Docker & Minikube, Log in to DockerHub Build and push the image, Deploy Kubernetes pods, and Port forward services

* * *

### 4\. Re-deploy with Existing Docker Image

`chmod 777 kube.sh
./kube.sh` 

This will:
Use an existing Docker image from DockerHub, Redeploy Kubernetes pods, Port forward services    

* * *

🪟 Windows Instructions (PowerShell or Git Bash)
------------------------------------------------

### 1\. Clone the repository

```bash
git clone https://github.com/KhushiGK/BankingSystem.git
git clone git@github.com:KhushiGK/BankingSystem.git
cd BankingSystem` 
``` 

### 2\. Set DockerHub image name

Edit the following files:

*   `k8s/deployment.yaml` → `image: <your-dockerhub-username>/banking-system:v1`
    
*   `k8s/react-deployment.yaml` → `image: <your-dockerhub-username>/banking-system:v1`
    

* * *

### 3\. Install Requirements

Manually install:
Docker Desktop, Minikube for Windows    

Start Docker Desktop and Minikube:

`minikube start` 

* * *

### 4\. Deploy Using Existing Image (Run in PowerShell/Git Bash)

`./kube.sh` 

> Note: If you want to build and push Docker image from Windows, manually run Docker build/push commands from `deploy.sh`.

* * *

🌐 Access the Services
----------------------

Service:
URL
Django -->[http://localhost:8000](http://localhost:8000)

React --> [http://localhost:3000](http://localhost:3000)

Prometheus--> [http://localhost:9090](http://localhost:9090)

Grafana --> [http://localhost:3030](http://localhost:3030)

Grafana Credentials:

*   **Username**: `admin`
    
*   **Password**: `admin`
    

* * *

✅ Done!
-------

Your BankingSystem app is up and running 🚀
