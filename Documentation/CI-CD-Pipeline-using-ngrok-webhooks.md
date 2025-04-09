# 🚀 Banking System - CI/CD Pipeline with Jenkins, Ngrok & Kubernetes

This part showcases a production-like CI/CD pipeline setup for a **Banking System** application using Jenkins, Docker, Kubernetes (Minikube), GitHub Webhooks, and Ngrok tunneling.

> 🔗 **Live Tunnel URL** (Ngrok): [https://3661-2405-201-c047-c859-8ece-d760-52a7-1787.ngrok-free.app](https://3661-2405-201-c047-c859-8ece-d760-52a7-1787.ngrok-free.app)

---

## 📦 Technologies Used

- **Django** (Backend Framework)
- **Celery + Redis** (Asynchronous Tasks)
- **PostgreSQL** (Database)
- **Docker** (Containerization)
- **Minikube + Kubernetes** (Orchestration)
- **Jenkins** (CI/CD automation)
- **Prometheus + Grafana** (Monitoring)
- **Ngrok** (Expose Jenkins server publicly)
- **GitHub Webhooks** (Trigger builds)

---

## ⚙️ CI/CD Pipeline Flow

### ✅ Trigger:
- Push to the `main` branch triggers a GitHub webhook.
- GitHub webhook hits the Ngrok URL (pointing to Jenkins).

### 🔁 Jenkins Pipeline Stages:

1. **Clone Repository**
   - Pulls latest code from GitHub.

2. **Build & Tag Docker Image**
   - Builds Docker image with version tag.

3. **Run Locally (Pre-Check)**
   - Starts the Docker container locally to verify functionality.

4. **Connect to Minikube**
   - Switch Docker context to Minikube’s Docker daemon.

5. **Deploy Application to K8s**
   - Applies Kubernetes manifests for Django, Celery Worker, Celery Beat.

6. **Deploy Monitoring Stack**
   - Prometheus & Grafana deployed to `monitoring` namespace.

7. **Start Celery Services**
   - Ensures worker & beat pods are running.

8. **Port Forwarding**
   - Forwards ports of Django, Prometheus, and Grafana services for local access.
---

## 🔐 GitHub Webhook Setup (with Ngrok)

1. Start Ngrok:
```bash
ngrok http 8080
```

![Screenshot (97)](https://github.com/user-attachments/assets/1b532db2-6235-4b56-9b25-ecc930600f1a)


2. Copy the public forwarding URL:
```
https://3661-2405-201-c047-c859-8ece-d760-52a7-1787.ngrok-free.app
```

3. On GitHub:
   - Go to **Settings > Webhooks**
   - Add webhook:
     - **Payload URL**: `https://xxxx.ngrok-free.app/github-webhook/`
     - **Content Type**: `application/json`
     - **Trigger on**: Just the push event

### Creating a Webhook on github :
![Screenshot (98)](https://github.com/user-attachments/assets/7b5f1e38-5a32-44f3-9eba-a2e301e399c8)

![Screenshot (96)](https://github.com/user-attachments/assets/442e7f2f-5e7f-42bb-88b7-2d6bc0d75c4a)

---

## Accessing Deployed Website from remote device  
![Screenshot (95)](https://github.com/user-attachments/assets/3f48fdbf-b722-4659-ba3f-0c7375751c36)

## Snapshots of Jenkins Build history
![Screenshot (100)](https://github.com/user-attachments/assets/3504baa0-b7ba-439f-8805-bebd6f7fe78a)
![image](https://github.com/user-attachments/assets/235ee6f3-984b-4395-96b3-653ac2a242bf)

## ✅ Best Practices Followed

- 🔐 Secrets are managed via Jenkins credentials
- 🧪 Local Docker run used for sanity before Kubernetes deployment
- 📊 Monitoring integrated for full observability
- ♻️ Declarative and idempotent Kubernetes YAMLs
---

> ⭐ Don't forget to star the repo if you found this helpful!

