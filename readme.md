# ☁️ CloudIQ – AI Enhanced Infrastructure for High Availability & Resilience

> Building intelligent, self-healing cloud infrastructure using Kubernetes, Prometheus, Grafana, and automated remediation.

![banner](screenshots/cloudiq_banner.png)

---

## ✨ Overview

**CloudIQ** is a cloud-native infrastructure automation framework designed to ensure **high availability, resilience, and self-healing** of microservices deployed on Kubernetes.  
It continuously monitors system health, detects abnormal behavior, triggers alerts, and automatically performs remediation actions such as **pod restarts and autoscaling**.

The project uses the **Sock Shop microservices application** as a realistic workload to demonstrate how modern cloud systems can recover from failures with minimal human intervention.

This project was developed as a **VTU Major Project (CSE)** and demonstrates real-world DevOps, SRE, and cloud engineering practices.

---

## 🧠 Why CloudIQ?

Modern cloud systems are:
- Highly distributed
- Dynamic and unpredictable
- Difficult to manage manually

Traditional monitoring tools are **reactive** and rely heavily on human operators.

💡 **CloudIQ changes this** by introducing:
- Continuous observability
- Alert-driven automation
- Closed-loop self-healing
- Dynamic autoscaling

---

## 🧩 Core Capabilities

| Capability | Description |
|----------|-------------|
| 📦 Cloud-Native Deployment | Microservices containerized with Docker and orchestrated using Kubernetes |
| 📊 Real-Time Monitoring | Prometheus scrapes CPU, memory, and pod metrics |
| 📈 Visualization & Alerting | Grafana dashboards and alert rules |
| 🤖 Automated Remediation | Custom Remediator service performs corrective actions |
| 🔁 Self-Healing | Automatic pod restart and recovery |
| ⚖️ Autoscaling | Kubernetes HPA scales pods based on CPU utilization |

---

## 🏗️ System Architecture

CloudIQ follows a **closed-loop automation architecture**:

1. Sock Shop microservices run on Kubernetes (EC2)
2. Prometheus collects real-time metrics
3. Grafana visualizes metrics and triggers alerts
4. Alerts are sent to the Remediator service
5. Remediator executes corrective actions
6. HPA scales pods dynamically
7. System returns to stable state

---

## 🛠️ Technology Stack

- **Cloud Platform**: AWS EC2  
- **OS**: Ubuntu 20.04 / 22.04  
- **Containerization**: Docker  
- **Orchestration**: Kubernetes (K3s)  
- **Monitoring**: Prometheus  
- **Visualization & Alerting**: Grafana  
- **Autoscaling**: Kubernetes HPA  
- **Remediation**: Custom Remediator Microservice  
- **Package Manager**: Helm  

---

## 📁 Project Structure

CloudIQ/
│
├── remediator/
│ ├── deploy-remediator.sh
│ ├── model.pkl
│ ├── app.py
│ └── Dockerfile
| ├── requirements.txt
│ └── remediator-deployment.yaml
│
├── Clouddeploy/
│ └── Cloud_setup.sh
│
├── screenshots/
│ ├── dashboard.png
│ ├── alert.png
│ └── autoscaling.png
│
└── README.md

---

## 📸 Screenshots

| Grafana Dashboard | CPU Alert Triggered | Pod Autoscaling |
|------------------|--------------------|-----------------|
| ![Dashboard](screenshots/dashboard.png) | ![Alert](screenshots/alert.png) | ![HPA](screenshots/autoscaling.png) |

---

## 🚀 Setup & Installation

### ✅ Prerequisites
- AWS EC2 instance (2 vCPU, 4+ GB RAM)
- Ubuntu OS
- Internet connectivity
- SSH access

---

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/CloudIQ.git
cd CloudIQ
```

### 2️⃣ Install Kubernetes (K3s)
* curl -sfL https://get.k3s.io | sh -
* sudo chmod 644 /etc/rancher/k3s/k3s.yaml
* mkdir -p ~/.kube
* sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config

### 3️⃣ Deploy Sock Shop Application
* kubectl create namespace sock-shop
* kubectl apply -f https://raw.githubusercontent.com/microservices-demo/microservices-demo/master/deploy/kubernetes/complete-demo.yaml -n sock-shop

### 4️⃣ Install Prometheus & Grafana
* helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
* helm repo add grafana https://grafana.github.io/helm-charts
* helm repo update

* helm install prometheus prometheus-community/prometheus -n monitoring --create-namespace
* helm install grafana grafana/grafana -n monitoring

### 5️⃣ Deploy Remediator
kubectl apply -f remediator/

### 6️⃣ Configure Autoscaling (HPA)
kubectl autoscale deployment remediator \
  --cpu-percent=80 \
  --min=1 \
  --max=3 \
  -n sock-shop

---

### 🌐 Access URLs
Service	URL
* Sock Shop	http://<EC2_PUBLIC_IP>:30001
* Prometheus	http://<EC2_PUBLIC_IP>:30900
* Grafana	http://<EC2_PUBLIC_IP>:32000

----

### Grafana Credentials:
Username: admin
Password: admin

---

### 🧪 Testing Scenarios
* High CPU stress testing
* Pod failure simulation
* Alert triggering validation
* Autoscaling verification
* End-to-end self-healing workflow

---

### 📈 Results & Impact
* Automated detection of performance issues
* Reduced Mean Time to Recovery (MTTR)
* Improved system availability
* Minimal manual intervention
* Demonstrated real-world cloud resilience

---

### ⚠️ Limitations
* Single-node Kubernetes cluster
* Autoscaling delay due to metric stabilization
* Predictive AI models not included in current version

---

### 🔮 Future Enhancements
* AI-based failure prediction
* Reinforcement learning for autoscaling
* Multi-node Kubernetes clusters
* Cost-aware scaling
* Distributed tracing integration

---

### 🎓 Academic Information
* Project Title: CloudIQ – AI Enhanced Infrastructure for High Availability and Resilience
* Department: Computer Science and Engineering
* Institution: Bapuji Institute of Engineering and Technology (BIET)
* University: Visvesvaraya Technological University (VTU)
* Location: Davangere, Karnataka, India

---

### 👨‍💻 Authors
Monika B S – monikabs4509@gmail.com

---

### 📜 License
This project is developed for academic and research purposes.
Free to use, modify, and extend with proper attribution.

---

⭐ If you find this project useful, consider giving it a star!


