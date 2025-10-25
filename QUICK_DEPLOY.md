# ⚡ Quick Deploy (5 Minutes)

## 🎯 **Fastest Way to Deploy**

### **Step 1: Push to GitHub** (1 minute)
```bash
cd C:\Users\gvina\Downloads\hackathonagent

# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for deployment"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/hackathon-agent.git
git branch -M main
git push -u origin main
```

---

### **Step 2: Deploy Backend to Render** (2 minutes)

1. Go to https://render.com/
2. Click **"Sign Up"** → Use GitHub
3. Click **"New +"** → **"Web Service"**
4. Click **"Connect GitHub"** → Select your repo
5. Fill in:
   ```
   Name: hackathon-agent-api
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```
6. Click **"Advanced"** → Add Environment Variables:
   ```
   ENVIRONMENT=production
   ELASTIC_CLOUD_ID=your-cloud-id-here
   ELASTIC_API_KEY=your-api-key-here
   CORS_ORIGINS=https://hackathon-agent.vercel.app
   ```
7. Click **"Create Web Service"**
8. **Copy your backend URL**: `https://hackathon-agent-api-xxxx.onrender.com`

---

### **Step 3: Deploy Frontend to Vercel** (2 minutes)

1. Go to https://vercel.com/
2. Click **"Sign Up"** → Use GitHub
3. Click **"Add New..."** → **"Project"**
4. Click **"Import"** on your repo
5. Fill in:
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   ```
6. Click **"Environment Variables"** → Add:
   ```
   NEXT_PUBLIC_API_URL=https://hackathon-agent-api-xxxx.onrender.com/api/v1
   ```
   (Use the URL from Step 2!)
   
7. Click **"Deploy"**
8. Wait 2 minutes → **Done!** 🎉

---

### **Step 4: Update Backend CORS** (30 seconds)

1. Go back to Render dashboard
2. Click your service → **"Environment"**
3. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```
   (Use your Vercel URL!)
4. Click **"Save Changes"**

---

## ✅ **You're Live!**

Your app is now deployed at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://hackathon-agent-api-xxxx.onrender.com`
- **API Docs**: `https://hackathon-agent-api-xxxx.onrender.com/api/v1/docs`

---

## 🧪 **Test It**

1. Open your Vercel URL
2. Try the chat
3. Check if API calls work
4. ✅ Everything should work!

---

## 🔄 **Future Updates**

Just push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push
```

Both Render and Vercel will **auto-deploy**! 🚀

---

## 💡 **Tips**

### Free Tier Limits:
- **Render**: 750 hours/month (enough for 24/7)
- **Vercel**: Unlimited deployments
- **Cost**: $0/month

### Performance:
- **First request**: ~30 seconds (Render cold start)
- **After that**: Fast!
- **Solution**: Keep it warm with uptime monitoring

### Monitoring:
- **Render**: Built-in logs and metrics
- **Vercel**: Built-in analytics
- **Both**: Email alerts on failures

---

## 🆘 **If Something Breaks**

### Backend won't start:
1. Check Render logs
2. Verify environment variables
3. Check `requirements.txt` is complete

### Frontend can't reach backend:
1. Check `NEXT_PUBLIC_API_URL` is correct
2. Check backend CORS includes frontend URL
3. Check backend is running (visit `/health`)

### CORS errors:
1. Update backend `CORS_ORIGINS`
2. Include both:
   - `https://your-app.vercel.app`
   - `https://your-app-git-main.vercel.app`

---

## 🎯 **For Hackathon Judges**

Add these to your submission:

**Live Demo**: `https://your-app.vercel.app`
**API Documentation**: `https://your-api.onrender.com/api/v1/docs`
**GitHub**: `https://github.com/YOUR_USERNAME/hackathon-agent`

**Deployment**: Vercel (Frontend) + Render (Backend)
**Status**: Production-ready, auto-deploying from GitHub

**This shows you know how to ship real products!** 🏆
