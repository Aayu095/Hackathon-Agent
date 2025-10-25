# 🚀 Deployment Guide (No Docker)

## **Option 1: Vercel + Render** ⭐ RECOMMENDED

### Why This Combo?
- ✅ **Free tier** for both
- ✅ **Easy setup** (10 minutes total)
- ✅ **Auto-deploy** from GitHub
- ✅ **Perfect for hackathons**
- ✅ **No credit card** needed

---

## 📦 **Part 1: Deploy Backend to Render**

### Step 1: Push to GitHub
```bash
cd C:\Users\gvina\Downloads\hackathonagent
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hackathon-agent.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your repository
5. Configure:
   - **Name**: `hackathon-agent-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

6. Add Environment Variables:
   ```
   ENVIRONMENT=production
   GOOGLE_CLOUD_PROJECT=
   ELASTIC_CLOUD_ID=your-cloud-id
   ELASTIC_API_KEY=your-api-key
   GITHUB_TOKEN=
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

7. Click **"Create Web Service"**
8. Wait 5-10 minutes for deployment
9. Copy your backend URL: `https://hackathon-agent-api.onrender.com`

---

## 🌐 **Part 2: Deploy Frontend to Vercel**

### Step 1: Update Frontend Environment

Edit `frontend/.env.production`:
```env
NEXT_PUBLIC_API_URL=https://hackathon-agent-api.onrender.com/api/v1
NEXT_PUBLIC_APP_NAME=Hackathon Agent
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Step 2: Deploy on Vercel

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click **"Add New"** → **"Project"**
4. Import your repository
5. Configure:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

6. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://hackathon-agent-api.onrender.com/api/v1
   ```

7. Click **"Deploy"**
8. Wait 2-3 minutes
9. Your app is live! 🎉

---

## 🔄 **Update Backend CORS**

After frontend is deployed, update backend environment on Render:

```
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-git-main.vercel.app
```

---

## **Option 2: Railway (Both Frontend + Backend)** 

### Why Railway?
- ✅ **Single platform** for both
- ✅ **$5 free credit** monthly
- ✅ **Easy setup**
- ✅ **Good performance**

### Deploy Backend:
1. Go to https://railway.app
2. Sign up with GitHub
3. **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repo
5. Add service → Select `backend` folder
6. Add environment variables
7. Deploy!

### Deploy Frontend:
1. Same project → **"New Service"**
2. Select `frontend` folder
3. Add environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy!

---

## **Option 3: Netlify + Render**

### Frontend on Netlify:
1. Go to https://netlify.com
2. **"Add new site"** → **"Import from Git"**
3. Select repo
4. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
5. Add environment variables
6. Deploy!

### Backend on Render:
- Same as Option 1

---

## 📋 **Pre-Deployment Checklist**

### Backend:
- [ ] `requirements.txt` is complete
- [ ] Environment variables are set
- [ ] CORS origins include frontend URL
- [ ] Port uses `$PORT` environment variable
- [ ] All API endpoints work locally

### Frontend:
- [ ] `.env.production` has correct API URL
- [ ] Build works locally (`npm run build`)
- [ ] No hardcoded localhost URLs
- [ ] API client uses environment variable

---

## 🧪 **Test Deployment**

### Backend Health Check:
```bash
curl https://your-backend.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "environment": "production"
}
```

### Frontend Test:
1. Open `https://your-app.vercel.app`
2. Try chat functionality
3. Check browser console for errors
4. Verify API calls work

---

## 🔧 **Troubleshooting**

### Backend Issues:

**Problem**: Build fails
```bash
# Solution: Check requirements.txt has all dependencies
pip freeze > requirements.txt
```

**Problem**: Port binding error
```bash
# Solution: Ensure using $PORT variable (already fixed)
port = int(os.environ.get("PORT", 8000))
```

**Problem**: CORS errors
```bash
# Solution: Add frontend URL to CORS_ORIGINS
CORS_ORIGINS=https://your-app.vercel.app
```

### Frontend Issues:

**Problem**: API calls fail
```bash
# Solution: Check NEXT_PUBLIC_API_URL is set correctly
# Must start with NEXT_PUBLIC_ to be available in browser
```

**Problem**: Build fails
```bash
# Solution: Run build locally first
cd frontend
npm run build
# Fix any errors shown
```

---

## 💰 **Cost Comparison**

| Platform | Backend | Frontend | Total |
|----------|---------|----------|-------|
| Vercel + Render | Free | Free | **$0/month** |
| Railway | $5 credit | $5 credit | **~$5/month** |
| Netlify + Render | Free | Free | **$0/month** |

**Recommendation**: Start with Vercel + Render (100% free!)

---

## 🚀 **Quick Deploy Commands**

### Push to GitHub:
```bash
git add .
git commit -m "Ready for deployment"
git push
```

### Trigger Redeploy:
- **Render**: Automatic on git push
- **Vercel**: Automatic on git push
- **Railway**: Automatic on git push

---

## 📊 **Deployment Status**

After deployment, you'll have:

```
Frontend: https://hackathon-agent.vercel.app
Backend:  https://hackathon-agent-api.onrender.com

Architecture:
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │ HTTPS
         ↓
┌─────────────────┐
│ Vercel (Frontend)│
│   - Next.js     │
│   - Static      │
└────────┬────────┘
         │ API Calls
         ↓
┌─────────────────┐
│ Render (Backend)│
│   - FastAPI     │
│   - Python      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  External APIs  │
│  - Elastic      │
│  - Vertex AI    │
│  - GitHub       │
└─────────────────┘
```

---

## ✅ **Final Steps**

1. Deploy backend to Render
2. Get backend URL
3. Update frontend `.env.production`
4. Deploy frontend to Vercel
5. Update backend CORS with frontend URL
6. Test everything works!

**Total Time**: ~15 minutes
**Cost**: $0 (free tier)

---

## 🎯 **For Your Hackathon Submission**

### Live Demo URLs:
```
Frontend: https://your-app.vercel.app
Backend API: https://your-api.onrender.com
API Docs: https://your-api.onrender.com/api/v1/docs
```

### Tech Stack:
- **Frontend**: Next.js 14 on Vercel
- **Backend**: FastAPI on Render
- **Database**: Elastic Cloud (Hosted)
- **AI**: Google Cloud Vertex AI
- **CI/CD**: GitHub → Auto-deploy

**This looks professional and production-ready!** 🏆
