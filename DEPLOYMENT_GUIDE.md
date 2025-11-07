# 🚀 Deployment Guide - Faith Brilliant Stars School

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Environment Configuration](#environment-configuration)
- [Database Migration](#database-migration)
- [Security Checklist](#security-checklist)
- [Monitoring & Maintenance](#monitoring--maintenance)

---

## ✅ Prerequisites

### System Requirements
- **OS:** Windows 10/11, Linux, or macOS
- **Python:** 3.9 or higher
- **Node.js:** 16.x or higher
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** 10GB free space

### Software Dependencies
```bash
# Python packages
pip install -r backend/requirements.txt

# Node packages
cd frontend && npm install
```

---

## 💻 Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd "Faith Brilliant Stars School"
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Initialize database
python create_db.py

# Run enhanced seed
python enhanced_seed.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Configure API URL
echo "VITE_API_URL=http://localhost:8001" > .env
```

### 4. Start Development Servers
```bash
# Option 1: Use batch script (Windows)
START_ENHANCED.bat

# Option 2: Manual start
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload --port 8001

# Terminal 2 - Frontend
cd frontend
npm run dev -- --port 5174
```

### 5. Verify Installation
- Frontend: http://localhost:5174
- Backend: http://localhost:8001
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

---

## 🌐 Production Deployment

### Option 1: Traditional Server Deployment

#### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.9 python3-pip python3-venv -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs -y

# Install Nginx
sudo apt install nginx -y

# Install PostgreSQL (recommended for production)
sudo apt install postgresql postgresql-contrib -y
```

#### 2. Backend Deployment
```bash
# Create application directory
sudo mkdir -p /var/www/faithschool
cd /var/www/faithschool

# Clone repository
git clone <repository-url> .

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Configure environment
cd backend
cp .env.example .env
nano .env  # Edit with production values

# Setup database
python create_db.py
python enhanced_seed.py

# Install Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/faithschool-backend.service
```

**Backend Service File:**
```ini
[Unit]
Description=Faith Brilliant Stars School Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/faithschool/backend
Environment="PATH=/var/www/faithschool/venv/bin"
ExecStart=/var/www/faithschool/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8001

[Install]
WantedBy=multi-user.target
```

```bash
# Start backend service
sudo systemctl start faithschool-backend
sudo systemctl enable faithschool-backend
sudo systemctl status faithschool-backend
```

#### 3. Frontend Deployment
```bash
cd /var/www/faithschool/frontend

# Install dependencies
npm install

# Build for production
npm run build

# Configure Nginx
sudo nano /etc/nginx/sites-available/faithschool
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name faithschool.rw www.faithschool.rw;

    # Frontend
    location / {
        root /var/www/faithschool/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # API Documentation
    location /docs {
        proxy_pass http://localhost:8001/docs;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/faithschool /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d faithschool.rw -d www.faithschool.rw

# Auto-renewal
sudo certbot renew --dry-run
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile (Backend)
```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

#### 2. Create Dockerfile (Frontend)
```dockerfile
# frontend/Dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### 3. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/faithschool
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./backend/uploads:/app/uploads

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=faithschool
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=faithschool
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### 4. Deploy with Docker
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## ⚙️ Environment Configuration

### Backend (.env)
```env
# Application
ENVIRONMENT=production
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/faithschool

# CORS
ALLOWED_ORIGINS=https://faithschool.rw,https://www.faithschool.rw

# JWT
JWT_SECRET_KEY=<generate-strong-jwt-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
UPLOAD_DIR=/var/www/faithschool/uploads
MAX_UPLOAD_SIZE=10485760

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@faithschool.rw
SMTP_PASSWORD=<email-password>

# SMS (Optional)
SMS_API_KEY=<sms-api-key>
SMS_SENDER_ID=FaithSchool

# Mobile Money (Optional)
MTN_MOMO_API_KEY=<mtn-api-key>
AIRTEL_MONEY_API_KEY=<airtel-api-key>
```

### Frontend (.env)
```env
VITE_API_URL=https://faithschool.rw/api
VITE_APP_NAME=Faith Brilliant Stars School
VITE_APP_VERSION=2.0.0
```

---

## 🗄️ Database Migration

### From SQLite to PostgreSQL

#### 1. Export SQLite Data
```bash
cd backend
python export_data.py
```

#### 2. Setup PostgreSQL
```bash
# Create database
sudo -u postgres psql
CREATE DATABASE faithschool;
CREATE USER faithschool WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE faithschool TO faithschool;
\q
```

#### 3. Update Configuration
```python
# backend/app/core/config.py
DATABASE_URL = "postgresql://faithschool:secure_password@localhost:5432/faithschool"
```

#### 4. Import Data
```bash
python import_data.py
```

---

## 🔒 Security Checklist

### Pre-Deployment
- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Update ALLOWED_ORIGINS for CORS
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up database backups
- [ ] Enable audit logging
- [ ] Review user permissions
- [ ] Test authentication flow
- [ ] Validate input sanitization

### Post-Deployment
- [ ] Monitor error logs
- [ ] Set up intrusion detection
- [ ] Configure rate limiting
- [ ] Enable DDoS protection
- [ ] Regular security updates
- [ ] Penetration testing
- [ ] Backup verification
- [ ] Disaster recovery plan

---

## 📊 Monitoring & Maintenance

### Logging Setup
```python
# backend/app/core/logging_config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/faithschool/app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Monitoring
```bash
# Create monitoring script
nano /usr/local/bin/check_faithschool.sh
```

```bash
#!/bin/bash
# Check backend
curl -f http://localhost:8001/health || systemctl restart faithschool-backend

# Check frontend
curl -f http://localhost || systemctl restart nginx

# Check database
pg_isready -h localhost -p 5432 || systemctl restart postgresql
```

```bash
# Add to crontab
crontab -e
*/5 * * * * /usr/local/bin/check_faithschool.sh
```

### Backup Strategy
```bash
# Database backup script
nano /usr/local/bin/backup_faithschool.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/faithschool"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump faithschool > "$BACKUP_DIR/db_$DATE.sql"

# Backup uploads
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /var/www/faithschool/uploads

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete
```

```bash
# Schedule daily backups
crontab -e
0 2 * * * /usr/local/bin/backup_faithschool.sh
```

### Performance Monitoring
```bash
# Install monitoring tools
pip install prometheus-fastapi-instrumentator

# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

## 🔄 Update Procedure

### 1. Backup Current System
```bash
# Backup database
pg_dump faithschool > backup_$(date +%Y%m%d).sql

# Backup code
tar -czf code_backup_$(date +%Y%m%d).tar.gz /var/www/faithschool
```

### 2. Pull Updates
```bash
cd /var/www/faithschool
git pull origin main
```

### 3. Update Dependencies
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
npm run build
```

### 4. Run Migrations
```bash
cd backend
alembic upgrade head
```

### 5. Restart Services
```bash
sudo systemctl restart faithschool-backend
sudo systemctl restart nginx
```

### 6. Verify
```bash
# Check health
curl http://localhost:8001/health

# Check logs
sudo journalctl -u faithschool-backend -f
```

---

## 🆘 Troubleshooting

### Backend Not Starting
```bash
# Check logs
sudo journalctl -u faithschool-backend -n 50

# Check port
sudo netstat -tulpn | grep 8001

# Test manually
cd /var/www/faithschool/backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U faithschool -d faithschool

# Check logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log
```

### Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Check logs
sudo tail -f /var/log/nginx/error.log

# Restart
sudo systemctl restart nginx
```

---

## 📞 Support

For deployment assistance:
- **Email:** info@faithschool.rw
- **Phone:** +250788123456
- **Documentation:** See other .md files in project root

---

*Last Updated: 2024*
*Version: 2.0.0*
