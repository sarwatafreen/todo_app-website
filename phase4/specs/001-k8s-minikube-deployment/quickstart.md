# Quickstart: Local Kubernetes Deployment for Todo AI Chatbot

**Feature**: 001-k8s-minikube-deployment
**Date**: 2026-02-05

## Prerequisites

1. Docker Desktop with Kubernetes enabled
2. Minikube installed
3. kubectl installed
4. Helm installed
5. kubectl-ai and kagent (optional but recommended for AI operations)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
git checkout 001-k8s-minikube-deployment
```

### 2. Start Minikube

```bash
minikube start
```

### 3. Verify Kubernetes Cluster

```bash
kubectl cluster-info
kubectl get nodes
```

### 4. Build Container Images (using AI assistance recommended)

```bash
# Build backend image
docker build -f Dockerfile.backend -t todo-backend:latest .

# Build frontend image
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

### 5. Deploy with Helm Charts

```bash
# Deploy backend
helm upgrade --install todo-backend ./helm/todo-backend/ --wait

# Deploy frontend
helm upgrade --install todo-frontend ./helm/todo-frontend/ --wait
```

### 6. Verify Deployment

```bash
# Check deployments
kubectl get deployments

# Check pods
kubectl get pods

# Check services
kubectl get services
```

### 7. Access the Application

```bash
# Get the frontend service NodePort
kubectl get services

# Access the application
minikube service todo-frontend --url
```

Or alternatively, use port forwarding:

```bash
kubectl port-forward svc/todo-frontend 3000:3000
```

## AI-Enhanced Operations

### Using kubectl-ai

```bash
# Scale the frontend to 3 replicas
kubectl-ai "scale deployment todo-frontend to 3 replicas"

# Check why pods are failing (if applicable)
kubectl-ai "check why pods are failing in todo-backend"

# Analyze resource usage
kubectl-ai "show me resource usage for all pods"
```

### Using kagent

```bash
# Analyze cluster health
kagent "analyze the cluster health"

# Optimize resource allocation
kagent "optimize resource allocation"
```

## Troubleshooting

### If Minikube won't start
- Ensure Docker Desktop is running with Kubernetes enabled
- Try `minikube delete` and then `minikube start`

### If services aren't accessible
- Check if pods are running: `kubectl get pods`
- Check service configuration: `kubectl describe service todo-frontend`

### If Docker builds fail
- Verify Dockerfile exists and is properly formatted
- Ensure Docker is running