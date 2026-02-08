#!/bin/bash
set -e

echo "🔄 Updating system..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "🐳 Installing K3s..."
curl -sfL https://get.k3s.io | sh -

echo "⏳ Waiting for K3s to be up..."
sleep 30

echo "🔍 Fixing kubeconfig permissions..."
sudo chmod 644 /etc/rancher/k3s/k3s.yaml
mkdir -p $HOME/.kube
sudo cp /etc/rancher/k3s/k3s.yaml $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

echo "⏳ Waiting for node to be Ready..."
kubectl wait --for=condition=Ready node --all --timeout=180s || true
kubectl get nodes -o wide

echo "🧹 Cleaning old Helm releases and namespaces..."
helm uninstall prometheus -n monitoring || true
helm uninstall grafana -n monitoring || true
kubectl delete namespace monitoring --ignore-not-found
kubectl delete namespace sock-shop --ignore-not-found
sleep 10

echo "📦 Creating namespaces..."
kubectl create namespace sock-shop
kubectl create namespace monitoring

echo "🚀 Deploying Sock Shop..."
kubectl apply -f https://raw.githubusercontent.com/microservices-demo/microservices-demo/master/deploy/kubernetes/complete-demo.yaml -n sock-shop

echo "📦 Installing Helm..."
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

echo "📦 Adding Helm repos..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
helm repo add grafana https://grafana.github.io/helm-charts || true
helm repo update

echo "🚀 Installing Prometheus (ultralight)..."
helm upgrade --install prometheus prometheus-community/prometheus -n monitoring \
  --set server.service.type=NodePort \
  --set server.service.nodePort=30900 \
  --set server.resources.requests.cpu=50m \
  --set server.resources.requests.memory=128Mi \
  --set server.resources.limits.cpu=100m \
  --set server.resources.limits.memory=256Mi

echo "🚀 Installing Grafana (ultralight)..."
helm upgrade --install grafana grafana/grafana -n monitoring \
  --set adminPassword=admin \
  --set service.type=NodePort \
  --set service.nodePort=32000 \
  --set resources.requests.cpu=25m \
  --set resources.requests.memory=64Mi \
  --set resources.limits.cpu=50m \
  --set resources.limits.memory=128Mi

echo "⏳ Waiting for monitoring pods..."
kubectl wait --for=condition=Ready pods --all -n monitoring --timeout=300s || true
kubectl get pods -n monitoring

echo "✅ Setup complete!"
echo "--------------------------------------------------------"
echo "🌐 Sock Shop Frontend: http://<EC2_PUBLIC_IP>:30001"
echo "🌐 Prometheus:        http://<EC2_PUBLIC_IP>:30900"
echo "🌐 Grafana:           http://<EC2_PUBLIC_IP>:32000"
echo "   Login → user: admin | pass: admin"
