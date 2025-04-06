#!/bin/bash

set -e

echo "🔍 Checking and installing Docker if not installed..."
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    sudo usermod -aG docker $USER
    echo "✅ Docker installed. Please log out and log back in if this is your first time installing Docker."
else
    echo "✅ Docker is already installed."
fi

echo "🔍 Checking and installing Minikube if not installed..."
if ! command -v minikube &> /dev/null; then
    echo "📦 Installing Minikube..."
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    rm minikube-linux-amd64
    echo "✅ Minikube installed."
else
    echo "✅ Minikube is already installed."
fi

echo "🧹 Cleaning up Minikube (if running)..."
minikube delete || true

echo "🚀 Starting Minikube..."
minikube start --force

echo "🔐 Logging into Docker..."
read -p "Docker Username: " DOCKER_USER
read -s -p "Docker Password: " DOCKER_PASS
echo
echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

# Docker Image Tag
IMAGE_NAME="banking-system"
DOCKER_TAG="$DOCKER_USER/$IMAGE_NAME:v1"

echo "🐳 Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

echo "🔁 Tagging and pushing image to Docker Hub..."
docker tag $IMAGE_NAME $DOCKER_TAG
docker push $DOCKER_TAG

echo "📦 Creating monitoring namespace..."
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

echo "📦 Applying Kubernetes manifests from k8s/"
kubectl apply -f k8s/

echo "⏳ Waiting for all pods to be ready..."
timeout=500
interval=10
elapsed=0
while true; do
    not_ready=$(kubectl get pods --all-namespaces | grep -v Running | grep -v Completed | wc -l)
    if [[ $not_ready -eq 1 ]]; then
        echo "✅ All pods are running!"
        break
    fi
    if [[ $elapsed -ge $timeout ]]; then
        echo "❌ Timeout waiting for pods to be ready."
        exit 1
    fi
    echo "⌛ Waiting... ($elapsed/$timeout seconds)"
    sleep $interval
    elapsed=$((elapsed + interval))
done

echo "📦 Applying Prometheus manifests..."
kubectl apply -f prometheus/ -n monitoring

echo "📦 Applying Grafana manifests..."
kubectl apply -f grafana/ -n monitoring

echo "⏳ Waiting for monitoring pods to be ready..."
timeout=500
elapsed=0
while true; do
    not_ready=$(kubectl get pods -n monitoring | grep -v Running | grep -v Completed | wc -l)
    if [[ $not_ready -eq 1 ]]; then
        echo "✅ All monitoring pods are running!"
        break
    fi
    if [[ $elapsed -ge $timeout ]]; then
        echo "❌ Timeout waiting for monitoring pods to be ready."
        exit 1
    fi
    echo "⌛ Waiting for monitoring pods... ($elapsed/$timeout seconds)"
    sleep $interval
    elapsed=$((elapsed + interval))
done

echo "🔁 Forwarding services in the background..."

kubectl port-forward svc/django-service 8000:8000 > /dev/null 2>&1 &
kubectl port-forward svc/react-service 3000:3000 > /dev/null 2>&1 &
kubectl port-forward svc/redis-exporter 9121:9121 > /dev/null 2>&1 &
kubectl port-forward svc/prometheus -n monitoring 9090:9090 > /dev/null 2>&1 &
kubectl port-forward svc/grafana -n monitoring 3030:3000 > /dev/null 2>&1 &

echo "✅ Deployment Complete!"
echo "🔗 Django App: http://localhost:8000"
echo "🔗 React Frontend: http://localhost:3000"
echo "📈 Prometheus: http://localhost:9090"
echo "username: admin"
echo "password: admin"
echo "📊 Grafana: http://localhost:3030"
