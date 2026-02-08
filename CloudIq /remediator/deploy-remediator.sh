#!/bin/bash
set -e
echo "🚀 Building Docker image..."
sudo docker build -t remediator:latest .

echo "📦 Saving image..."
sudo docker save -o remediator.tar remediator:latest

echo "📥 Importing into K3s..."
sudo k3s ctr images import remediator.tar

echo "🗑️ Removing old deployment..."
kubectl delete deploy remediator -n sock-shop --ignore-not-found
kubectl delete svc remediator -n sock-shop --ignore-not-found

echo "🚀 Deploying new version..."
kubectl apply -f remediator-deployment.yaml

kubectl rollout status deploy/remediator -n sock-shop
kubectl get pods -n sock-shop -l app=remediator
