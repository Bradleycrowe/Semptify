# GitHub Actions / CI-CD Configuration Examples

## 📦 Docker Deployment Example

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p logs security uploads copilot_sync final_notices data

# Expose port
EXPOSE 8080

# Environment
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run server
CMD ["python", "start_production.py"]
```

### Build and Run:

```bash
# Build image
docker build -t semptify:latest .

# Run container
docker run -p 8080:8080 \
  -e FLASK_SECRET="your-secret" \
  -e SECURITY_MODE="enforced" \
  semptify:latest

# Access
curl http://localhost:8080
```

---

## 🔄 GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Semptify Production

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Run tests
      run: pytest -v --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      env:
        DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
        DEPLOY_USER: ${{ secrets.DEPLOY_USER }}
      run: |
        mkdir -p ~/.ssh
        echo "$DEPLOY_KEY" > ~/.ssh/deploy_key
        chmod 600 ~/.ssh/deploy_key
        ssh-keyscan -H $DEPLOY_HOST >> ~/.ssh/known_hosts
        
        ssh -i ~/.ssh/deploy_key $DEPLOY_USER@$DEPLOY_HOST << 'EOF'
        cd /var/www/semptify
        git pull origin main
        source .venv/bin/activate
        pip install -r requirements.txt
        sudo systemctl restart semptify
        sleep 5
        curl -f http://localhost:8080/health || exit 1
        EOF
```

---

## 🐳 Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  semptify:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: semptify
    ports:
      - "8080:8080"
    environment:
      FLASK_ENV: production
      FLASK_SECRET: ${FLASK_SECRET}
      SECURITY_MODE: enforced
      SEMPTIFY_THREADS: 4
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
      - ./security:/app/security
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Usage:

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f semptify

# Stop
docker-compose down
```

---

## 📦 Render.com Deployment

Create `render.yaml`:

```yaml
services:
  - type: web
    name: semptify
    env: python
    plan: standard
    buildCommand: pip install -r requirements.txt
    startCommand: python start_production.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_SECRET
        scope: build
      - key: SECURITY_MODE
        value: enforced
      - key: PORT
        value: 8080
```

### Deploy:

```bash
# Connect Render to GitHub repo
# Render auto-deploys on push to main
```

---

## ☁️ AWS Deployment (EC2)

```bash
#!/bin/bash
# Deploy script for AWS EC2

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Clone repository
cd /opt
sudo git clone https://github.com/Bradleycrowe/Semptify.git
cd Semptify

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/semptify.service > /dev/null << EOF
[Unit]
Description=Semptify Production Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/Semptify
Environment="PATH=/opt/Semptify/.venv/bin"
Environment="FLASK_ENV=production"
Environment="FLASK_SECRET=$(openssl rand -hex 32)"
Environment="SECURITY_MODE=enforced"
ExecStart=/opt/Semptify/.venv/bin/python start_production.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable semptify
sudo systemctl start semptify

# Check status
sudo systemctl status semptify
```

---

## 🏗️ Azure App Service

### Using Azure CLI:

```bash
#!/bin/bash

# Variables
RESOURCE_GROUP="semptify-rg"
APP_NAME="semptify-app"
LOCATION="eastus"

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Create App Service plan
az appservice plan create \
  --name semptify-plan \
  --resource-group $RESOURCE_GROUP \
  --sku B2 \
  --is-linux

# Create web app
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan semptify-plan \
  --name $APP_NAME \
  --runtime "python|3.11"

# Configure startup command
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --startup-file "python start_production.py"

# Set environment variables
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings \
    FLASK_ENV=production \
    SECURITY_MODE=enforced \
    WEBSITE_PORT=8080

# Deploy from Git
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --src deployment.zip
```

---

## 🔧 Kubernetes (k8s) Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: semptify-config
data:
  FLASK_ENV: "production"
  SECURITY_MODE: "enforced"
  SEMPTIFY_THREADS: "4"

---
apiVersion: v1
kind: Secret
metadata:
  name: semptify-secrets
type: Opaque
stringData:
  FLASK_SECRET: "your-secret-here"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: semptify
  labels:
    app: semptify
spec:
  replicas: 2
  selector:
    matchLabels:
      app: semptify
  template:
    metadata:
      labels:
        app: semptify
    spec:
      containers:
      - name: semptify
        image: semptify:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: semptify-config
        - secretRef:
            name: semptify-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
apiVersion: v1
kind: Service
metadata:
  name: semptify-service
spec:
  type: LoadBalancer
  selector:
    app: semptify
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
kubectl get pods -l app=semptify
kubectl logs -f deployment/semptify
```

---

## 📋 Environment Secrets for CI/CD

Add to GitHub Secrets (Settings → Secrets → Actions):

```
FLASK_SECRET = <generated-secret>
DEPLOY_HOST = production.example.com
DEPLOY_USER = deploy
DEPLOY_KEY = <private-ssh-key>
```

---

## 🔍 Health Check Endpoint

Add to your Flask app if not already present:

```python
@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }, 200

@app.route('/readyz')
def ready():
    # Check if app is ready to serve
    return {
        'status': 'ready'
    }, 200
```

---

## 📊 Monitoring Setup

### Prometheus Metrics

Add to start_production.py:

```python
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

---

## 🚀 Deployment Checklist

- [ ] Dockerfile tested locally
- [ ] CI/CD pipeline configured
- [ ] Environment secrets set up
- [ ] Health endpoints working
- [ ] Logs being collected
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Rollback procedure documented
- [ ] Load balancing configured (if needed)
- [ ] SSL/TLS certificates configured

---

**Version**: 1.0
**Last Updated**: November 4, 2025
