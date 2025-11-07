# Deployment Guide

## Production Deployment

### Prerequisites
- Domain name configured
- SSL certificates
- Production database (Supabase or managed PostgreSQL)
- Cloudflare account (frontend)
- Render account (backend)

### Backend Deployment (Render)

1. **Create PostgreSQL Database**
   - Sign up for Supabase or use Render's PostgreSQL
   - Note the connection string

2. **Deploy Backend to Render**
   ```bash
   # Push code to GitHub
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

3. **Configure Render**
   - Create new Web Service
   - Connect GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables from `.env.example`

4. **Run Migrations**
   ```bash
   # SSH into Render or use Render Shell
   alembic upgrade head
   python seed.py
   ```

### Frontend Deployment (Cloudflare Pages)

1. **Build Frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy to Cloudflare Pages**
   - Connect GitHub repository
   - Build command: `npm run build`
   - Build output directory: `build`
   - Add environment variable: `VITE_API_URL=<your-backend-url>`

### Environment Variables

**Backend (Production)**
```env
DATABASE_URL=<supabase-or-render-postgres-url>
SECRET_KEY=<generate-strong-secret-key>
ENVIRONMENT=production
DEBUG=False
ALLOWED_ORIGINS=https://your-domain.com
SENDGRID_API_KEY=<your-sendgrid-key>
TWILIO_ACCOUNT_SID=<your-twilio-sid>
TWILIO_AUTH_TOKEN=<your-twilio-token>
MTN_MOMO_API_KEY=<your-mtn-key>
SENTRY_DSN=<your-sentry-dsn>
```

**Frontend (Production)**
```env
VITE_API_URL=https://api.your-domain.com
```

### SSL/TLS Configuration
- Cloudflare automatically provides SSL for frontend
- Render provides SSL for backend
- Ensure HTTPS is enforced

### Monitoring

1. **Sentry Setup**
   - Create Sentry project
   - Add DSN to backend environment variables
   - Errors will be tracked automatically

2. **Health Checks**
   - Backend: `https://api.your-domain.com/health`
   - Set up uptime monitoring (UptimeRobot, Pingdom)

### Backup Strategy

1. **Database Backups**
   - Supabase: Automatic daily backups
   - Render PostgreSQL: Configure backup schedule

2. **File Backups**
   - Use S3 or Cloudflare R2 for uploaded files
   - Configure automatic backups

### Scaling

1. **Backend Scaling**
   - Render: Upgrade to higher tier for more resources
   - Add Redis for caching
   - Use Celery for background tasks

2. **Database Scaling**
   - Supabase: Upgrade plan for more connections
   - Add read replicas if needed

### Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY (min 32 characters)
- [ ] Enable HTTPS only
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable database encryption
- [ ] Regular security updates
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerts

### Post-Deployment

1. Test all features in production
2. Verify mobile money integration
3. Test SMS/Email notifications
4. Check offline functionality
5. Verify report generation
6. Test with low-bandwidth connection
7. Validate on mobile devices

### Rollback Plan

If deployment fails:
```bash
# Backend
git revert HEAD
git push origin main

# Frontend
# Cloudflare Pages allows instant rollback to previous deployment
```

### Support

For deployment issues:
- Check logs in Render dashboard
- Review Cloudflare Pages build logs
- Monitor Sentry for errors
- Check database connection status
