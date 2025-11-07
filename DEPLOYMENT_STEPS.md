# 🚀 DEPLOYMENT GUIDE - Faith Brilliant Stars School

## Step 1: GitHub Setup
1. Create repository at https://github.com/new
   - Name: `faith-brilliant-stars-school`
   - Public repository
   - Don't initialize with README

2. Push code:
```bash
git remote add origin https://github.com/Leonardus437/faith-brilliant-stars-school.git
git push -u origin main
```

## Step 2: Backend Deployment (Render)
1. Go to https://render.com
2. Connect your GitHub account
3. Click "New Web Service"
4. Select your repository: `faith-brilliant-stars-school`
5. Configure:
   - **Name**: `faith-brilliant-stars-school-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python full_seed.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Auto-Deploy**: `Yes`

6. Add Environment Variables:
   - `DATABASE_URL`: `sqlite:///./faithschool.db`
   - `SECRET_KEY`: (Generate a secure key)
   - `ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`

## Step 3: Frontend Deployment (Cloudflare Pages)
1. Go to https://pages.cloudflare.com
2. Connect to Git → GitHub
3. Select repository: `faith-brilliant-stars-school`
4. Configure:
   - **Project name**: `faith-brilliant-stars-school`
   - **Production branch**: `main`
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Build output directory**: `frontend/build`
   - **Root directory**: `/`

5. Add Environment Variables:
   - `VITE_API_URL`: `https://faith-brilliant-stars-school-backend.onrender.com`

## Step 4: Auto-Deployment Setup
Both services will auto-deploy on every push to `main` branch.

## Step 5: Update API URL
After backend deployment, update frontend environment:
1. Get your Render backend URL
2. Update `frontend/.env.production` with actual URL
3. Commit and push changes

## 🎯 Live URLs (After Deployment)
- **Frontend**: https://faith-brilliant-stars-school.pages.dev
- **Backend**: https://faith-brilliant-stars-school-backend.onrender.com
- **API Docs**: https://faith-brilliant-stars-school-backend.onrender.com/docs

## 🔧 GitHub Secrets (Optional - for GitHub Actions)
Add these secrets in GitHub repository settings:
- `RENDER_SERVICE_ID`: Your Render service ID
- `RENDER_API_KEY`: Your Render API key
- `CLOUDFLARE_API_TOKEN`: Your Cloudflare API token
- `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare account ID