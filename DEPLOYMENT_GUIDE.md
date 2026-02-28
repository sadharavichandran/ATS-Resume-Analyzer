# 🌐 Deployment & Environment Setup Guide

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Production Environment Variables](#production-environment-variables)
3. [Cloud Deployments](#cloud-deployments)
4. [Docker Containerization](#docker-containerization)
5. [Database Migration](#database-migration)
6. [Security Hardening](#security-hardening)
7. [Monitoring & Logging](#monitoring--logging)
8. [Scaling & Performance](#scaling--performance)
9. [Backup & Recovery](#backup--recovery)
10. [Troubleshooting Deployment](#troubleshooting-deployment)

---

## Local Development Setup

### Windows Setup

#### 1. Install Python

```powershell
# Download and install from python.org
# OR use Windows Package Manager
winget install Python.Python.3.11

# Verify installation
python --version
# Output: Python 3.11.x
```

#### 2. Create Project Directory

```powershell
# Create and navigate to project folder
mkdir C:\Projects\ats-analyzer
cd C:\Projects\ats-analyzer

# (or use existing directory with code)
```

#### 3. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If script is blocked, run as Administrator:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify all packages installed
pip list
```

#### 5. Run Application

```powershell
# Run Streamlit app
streamlit run app.py

# Output: You can now view your Streamlit app in your browser.
#         URL: http://localhost:8501
```

### macOS Setup

#### 1. Install Python (via Homebrew)

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Verify installation
python3 --version
```

#### 2. Create Project Directory & Virtual Environment

```bash
# Create and navigate to project
mkdir ~/Projects/ats-analyzer
cd ~/Projects/ats-analyzer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Prompt should show (venv) at the beginning
```

#### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify
pip list
```

#### 4. Run Application

```bash
streamlit run app.py

# Open: http://localhost:8501
```

### Linux Setup (Ubuntu/Debian)

#### 1. Install Python & Dependencies

```bash
# Update package manager
sudo apt update
sudo apt upgrade -y

# Install Python and build tools
sudo apt install python3.11 python3.11-venv python3.11-dev build-essential -y

# Verify
python3 --version
```

#### 2. Create Project & Virtual Environment

```bash
# Create project directory
mkdir ~/ats-analyzer
cd ~/ats-analyzer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

#### 4. Run Application

```bash
# Run app with nohup for background execution
nohup streamlit run app.py > app.log 2>&1 &

# Or simple foreground run
streamlit run app.py

# Access: http://localhost:8501
```

---

## Production Environment Variables

### Create .env File

```bash
# Create environment file
touch .env

# Or on Windows
New-Item -Path .env -ItemType File
```

### Environment Variables Template

```bash
# ===============================================
# ATS Resume Analyzer - Production Configuration
# ===============================================

# --- Server Configuration ---
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_BASEURL=https://yourdomain.com
STREAMLIT_SERVER_ENABLECORS=false
STREAMLIT_SERVER_ENABLEXSRFPROTECTION=true

# --- Security ---
SECRET_KEY=your-secret-key-generate-with-secrets.token_urlsafe-32
SESSION_TIMEOUT=3600  # seconds
MAX_LOGIN_ATTEMPTS=5
LOGIN_ATTEMPT_LOCKOUT=900  # seconds

# --- Database (Future Migration) ---
DATABASE_URL=postgresql://user:password@localhost:5432/ats_analyzer
DB_POOL_SIZE=5
DB_POOL_TIMEOUT=30

# --- Email Service (for password reset) ---
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@yourdomain.com

# --- AWS/Cloud (if using cloud storage) ---
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=ats-analyzer-uploads

# --- Analytics (optional) ---
SENTRY_DSN=https://key@sentry.io/project
GOOGLE_ANALYTICS_ID=your-ga-id

# --- Logging ---
LOG_LEVEL=INFO
LOG_FILE=/var/log/ats-analyzer.log

# --- Features (flags) ---
FEATURE_BATCH_UPLOAD=false
FEATURE_EMAIL_REPORTS=false
FEATURE_TEAM_WORKSPACES=false
```

### Load Environment Variables

#### Using python-dotenv

```python
# In app.py
from dotenv import load_dotenv
import os

load_dotenv()

# Access variables
secret_key = os.getenv('SECRET_KEY')
db_url = os.getenv('DATABASE_URL')
```

#### Windows PowerShell

```powershell
# Load from .env file (manual)
$env_vars = Get-Content .env | ConvertFrom-StringData
foreach ($var in $env_vars.GetEnumerator()) {
    [Environment]::SetEnvironmentVariable($var.Key, $var.Value)
}

# Verify
$env:SECRET_KEY
```

#### Linux/macOS

```bash
# Load environment from .env
export $(cat .env | xargs)

# Verify
echo $SECRET_KEY

# Or use in command directly
$(cat .env) streamlit run app.py
```

---

## Cloud Deployments

### Streamlit Cloud (Easiest)

#### Setup Steps

```bash
# 1. Push code to GitHub
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Click "New App"
# 4. Select GitHub repository
# 5. Select branch and main file (app.py)
# 6. Click Deploy!

# Your app is now live at:
# https://app-name-username.streamlit.app
```

#### Streamlit Cloud Configuration

Create `streamlit.toml`:

```toml
[client]
showErrorDetails = false
toolbarMode = "viewer"

[logger]
level = "info"

[theme]
primaryColor = "#0066ff"
backgroundColor = "#0f0f1e"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#e0e0e0"
font = "sans serif"

[server]
port = 8501
headless = true
runOnSave = true
maxUploadSize = 200
enableCORS = true
```

#### GitHub Actions for CI/CD

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest tests/ -v

      - name: Deploy to Streamlit Cloud
        env:
          STREAMLIT_EMAIL: ${{ secrets.STREAMLIT_EMAIL }}
          STREAMLIT_PASSWORD: ${{ secrets.STREAMLIT_PASSWORD }}
        run: |
          streamlit deploy --share

      - name: Notify deployment
        run: echo "✅ Deployed successfully!"
```

### Heroku Deployment

#### Step 1: Create Procfile

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### Step 2: Create app.json

```json
{
  "name": "ATS Resume Analyzer",
  "description": "Resume analysis with ATS scoring",
  "repository": "https://github.com/username/ats-analyzer",
  "keywords": ["streamlit", "resume", "ats"],
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ],
  "env": {
    "STREAMLIT_SERVER_ENABLECORS": {
      "description": "No CORS required",
      "value": "false"
    },
    "STREAMLIT_SERVER_HEADLESS": {
      "description": "Run headless",
      "value": "true"
    }
  }
}
```

#### Step 3: Deploy

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Monitor logs
heroku logs --tail
```

### AWS Deployment

#### Using Elastic Beanstalk

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Initialize EB application
eb init -p "Python 3.11 running on 64bit Amazon Linux 2" ats-analyzer

# 3. Create environment
eb create ats-analyzer-env

# 4. Deploy
git push origin main  # EB auto-deploys on push

# 5. Open application
eb open
```

Create `.ebextensions/python.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH
```

### Google Cloud Run

```dockerfile
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Configure Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "port = 8080" >> ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml

# Expose port
EXPOSE 8080

# Run app
CMD streamlit run app.py
```

Deploy:

```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT-ID/ats-analyzer

# Deploy to Cloud Run
gcloud run deploy ats-analyzer \
  --image gcr.io/PROJECT-ID/ats-analyzer \
  --platform managed \
  --region us-central1 \
  --memory 512Mi
```

---

## Docker Containerization

### Dockerfile (Complete)

```dockerfile
# ========================================
# ATS Resume Analyzer - Docker Image
# ========================================

FROM python:3.11-slim

LABEL maintainer="Your Name <email@example.com>"
LABEL description="ATS Resume Analyzer with Dark Theme"
LABEL version="3.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY auth_system.py .
COPY resume_analyzer.py .
COPY recommendations.py .
COPY skills.py .
COPY users_db.json .

# Create .streamlit directory
RUN mkdir -p ~/.streamlit

# Configure Streamlit
RUN echo "\
[server]\n\
port = 8501\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = true\n\
\n\
[theme]\n\
primaryColor = '#0066ff'\n\
backgroundColor = '#0f0f1e'\n\
secondaryBackgroundColor = '#1a1a2e'\n\
textColor = '#e0e0e0'\n\
" > ~/.streamlit/config.toml

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
```

### Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  app:
    build: .
    container_name: ats-analyzer
    ports:
      - "8501:8501"
    environment:
      STREAMLIT_SERVER_PORT: 8501
      STREAMLIT_SERVER_HEADLESS: "true"
    volumes:
      - ./:/app
      - ~/.streamlit:/root/.streamlit
    networks:
      - ats-network
    restart: unless-stopped

  # Optional: PostgreSQL database
  postgres:
    image: postgres:15-alpine
    container_name: ats-db
    environment:
      POSTGRES_USER: ats_user
      POSTGRES_PASSWORD: secure_password_here
      POSTGRES_DB: ats_analyzer
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - ats-network
    restart: unless-stopped

networks:
  ats-network:
    driver: bridge

volumes:
  postgres_data:
```

### Build & Run Commands

```bash
# Build image
docker build -t ats-analyzer:3.0 .

# Run container
docker run -p 8501:8501 ats-analyzer:3.0

# Run with environment file
docker run -p 8501:8501 --env-file .env ats-analyzer:3.0

# Run with volume (persist data)
docker run -p 8501:8501 -v $(pwd)/data:/app/data ats-analyzer:3.0

# Using docker-compose
docker-compose up -d

# View logs
docker logs ats-analyzer

# Stop container
docker stop ats-analyzer
docker rm ats-analyzer

# Push to Docker Hub
docker login
docker tag ats-analyzer:3.0 username/ats-analyzer:3.0
docker push username/ats-analyzer:3.0
```

---

## Database Migration

### PostgreSQL Setup (Production Database)

#### Installation

```bash
# macOS (via Homebrew)
brew install postgresql@15

# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# Windows
# Download from postgresql.org

# Verify installation
psql --version
```

#### Create Database & User

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE ats_analyzer;

# Create user
CREATE USER ats_user WITH PASSWORD 'secure_password';

# Grant privileges
ALTER ROLE ats_user SET client_encoding TO 'utf8';
ALTER ROLE ats_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ats_user SET default_transaction_deferrable TO on;
ALTER ROLE ats_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE ats_analyzer TO ats_user;

# Exit psql
\q
```

#### Database Schema

Create `schema.sql`:

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    analyses_count INT DEFAULT 0
);

-- Resume Analysis Table
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    candidate_name VARCHAR(255),
    resume_text TEXT,
    job_description TEXT,
    ats_score DECIMAL(5, 2),
    match_percentage DECIMAL(5, 2),
    found_skills JSON,
    missing_skills JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);

-- Create audit table
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(255),
    details JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Execute schema:

```bash
psql -U ats_user -d ats_analyzer -f schema.sql
```

### Update auth_system.py for PostgreSQL

```python
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://ats_user:password@localhost:5432/ats_analyzer')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def register_user(email: str, password: str, full_name: str) -> tuple:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "Email already registered"

            # Hash password
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            # Create user
            cursor.execute(
                """INSERT INTO users (email, password_hash, full_name)
                   VALUES (%s, %s, %s)""",
                (email, password_hash, full_name)
            )
            conn.commit()

            return True, "Registration successful"

    except psycopg2.Error as e:
        return False, f"Database error: {str(e)}"

def login_user(email: str, password: str) -> tuple:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute(
                "SELECT password_hash, full_name FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()

            if not user:
                return False, "User not found"

            if bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
                return True, user['full_name']

            return False, "Incorrect password"

    except psycopg2.Error as e:
        return False, f"Database error: {str(e)}"
```

---

## Security Hardening

### SSL/TLS Certificate

```bash
# Using Let's Encrypt with Certbot
sudo certbot certonly --standalone -d yourdomain.com

# Configure Streamlit for HTTPS
echo "[server]" >> ~/.streamlit/config.toml
echo "sslCertFile = /path/to/cert.pem" >> ~/.streamlit/config.toml
echo "sslKeyFile = /path/to/key.pem" >> ~/.streamlit/config.toml
```

### nginx Reverse Proxy

Create `/etc/nginx/sites-available/ats-analyzer`:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/ats-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Monitoring & Logging

### Systemd Service File

Create `/etc/systemd/system/ats-analyzer.service`:

```ini
[Unit]
Description=ATS Resume Analyzer
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/ats-analyzer
Environment="PATH=/opt/ats-analyzer/venv/bin"
ExecStart=/opt/ats-analyzer/venv/bin/streamlit run app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ats-analyzer
sudo systemctl start ats-analyzer
sudo systemctl status ats-analyzer
```

### Logging Setup

Add to `app.py`:

```python
import logging
import logging.handlers

# Configure logging
logger = logging.getLogger("ats_analyzer")
logger.setLevel(logging.DEBUG)

# File handler
handler = logging.handlers.RotatingFileHandler(
    'logs/ats.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Usage
logger.info("User logged in")
logger.error("Analysis failed")
```

---

## Scaling & Performance

### Load Balancing (nginx)

```nginx
upstream streamlit_backend {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://streamlit_backend;
        proxy_set_header Host $host;
    }
}
```

### Caching Strategy

```python
@st.cache_data(ttl=3600)
def get_recommendations(skill):
    return LEARNING_RESOURCES.get(skill, [])

@st.cache_resource
def initialize_ml_models():
    return TfidfVectorizer()
```

### Database Connection Pooling

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600
)
```

---

## Backup & Recovery

### Backup Script

Create `backup.sh`:

```bash
#!/bin/bash

# Database backup
BACKUP_DIR="/backups/ats-analyzer"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump -U ats_user ats_analyzer | gzip > "$BACKUP_DIR/ats_db_$TIMESTAMP.sql.gz"

# Application files backup
tar -czf "$BACKUP_DIR/ats_app_$TIMESTAMP.tar.gz" /opt/ats-analyzer

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $TIMESTAMP"
```

Schedule with cron:

```bash
# Daily backup at 2 AM
0 2 * * * /opt/ats-analyzer/backup.sh
```

---

## Troubleshooting Deployment

### Common Issues

#### 1. Port Already in Use

```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>
```

#### 2. Database Connection Failed

```python
# Test connection
import psycopg2

try:
    conn = psycopg2.connect("postgresql://user:pass@localhost/db")
    print("✅ Connected")
except psycopg2.Error as e:
    print(f"❌ Error: {e}")
```

#### 3. High Memory Usage

```bash
# Monitor memory
top -b -n 1 | grep streamlit

# Optimize:
# - Disable caching if not needed
# - Use session state efficiently
# - Clear large variables
```

#### 4. Slow PDF Processing

```python
# Add timeout
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("PDF processing timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout

try:
    extract_text(pdf_file)
finally:
    signal.alarm(0)  # Cancel alarm
```

---

## Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created with production variables
- [ ] `users_db.json` created or database configured
- [ ] SSL certificate obtained (for HTTPS)
- [ ] nginx/reverse proxy configured
- [ ] Systemd service created
- [ ] Monitoring/logging configured
- [ ] Backup strategy implemented
- [ ] Tested with sample resumes
- [ ] Database optimized with indexes
- [ ] Backup automated with cron
- [ ] SSL certificate auto-renewal set up (certbot)
- [ ] Rate limiting configured
- [ ] CDN configured (optional)
- [ ] Monitoring alerts configured

---

**Deployment Guide v3.0**  
**Last Updated**: February 28, 2025  
**Status**: Complete & Production Ready
