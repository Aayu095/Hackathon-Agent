# ✅ Deployment Checklist

## 📋 **Before You Deploy**

### Backend Ready?
- [ ] All dependencies in `requirements.txt`
- [ ] Environment variables documented
- [ ] Health endpoint works (`/health`)
- [ ] CORS configured
- [ ] Port uses `$PORT` variable ✅ (already done)
- [ ] No hardcoded secrets in code
- [ ] Fallback system working ✅ (already done)

### Frontend Ready?
- [ ] Build works locally (`npm run build`)
- [ ] `.env.production` created ✅ (already done)
- [ ] No hardcoded localhost URLs
- [ ] API client uses environment variable ✅ (already done)
- [ ] All pages load correctly

### External Services?
- [ ] Elastic Cloud ID and API Key ready
- [ ] GitHub token (optional)
- [ ] Google Cloud credentials (optional - fallback works)

---

## 🚀 **Deployment Steps**

### 1. GitHub Setup
- [ ] Repository created
- [ ] Code pushed to main branch
- [ ] `.gitignore` excludes `.env` files
- [ ] README updated with deployment info

### 2. Backend Deployment (Render)
- [ ] Account created on Render
- [ ] Web service created
- [ ] Repository connected
- [ ] Build command set
- [ ] Start command set
- [ ] Environment variables added
- [ ] Deployment successful
- [ ] Backend URL copied

### 3. Frontend Deployment (Vercel)
- [ ] Account created on Vercel
- [ ] Project imported
- [ ] Root directory set to `frontend`
- [ ] Environment variable `NEXT_PUBLIC_API_URL` added
- [ ] Deployment successful
- [ ] Frontend URL copied

### 4. Final Configuration
- [ ] Backend CORS updated with frontend URL
- [ ] Frontend tested with backend
- [ ] All features working
- [ ] No console errors

---

## 🧪 **Testing Checklist**

### Backend Tests:
```bash
# Health check
curl https://your-backend.onrender.com/health

# API docs
open https://your-backend.onrender.com/api/v1/docs

# Chat endpoint
curl -X POST https://your-backend.onrender.com/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}'
```

Expected: All return 200 OK

### Frontend Tests:
- [ ] Homepage loads
- [ ] Chat page loads
- [ ] Settings modal opens
- [ ] New chat works
- [ ] Can send messages
- [ ] Receives responses
- [ ] No CORS errors
- [ ] No 404 errors

---

## 📊 **Deployment URLs**

Fill these in after deployment:

```
Frontend URL: https://_________________.vercel.app
Backend URL:  https://_________________.onrender.com
API Docs:     https://_________________.onrender.com/api/v1/docs
GitHub Repo:  https://github.com/_________________
```

---

## 🎯 **For Hackathon Submission**

### Required Info:
- [x] Live demo URL
- [x] GitHub repository
- [x] Video demo (record after deployment)
- [x] Screenshots
- [x] Tech stack description

### Submission Template:
```
🚀 Live Demo: https://your-app.vercel.app
📚 API Docs: https://your-api.onrender.com/api/v1/docs
💻 GitHub: https://github.com/YOUR_USERNAME/hackathon-agent
🎥 Video: [Your video link]

Tech Stack:
- Frontend: Next.js 14, React 18, TailwindCSS
- Backend: FastAPI, Python 3.12
- Search: Elastic Cloud (Hybrid Search)
- AI: Google Cloud Vertex AI (Gemini Pro)
- Deployment: Vercel + Render
- CI/CD: GitHub Auto-deploy

Features:
✅ Idea Validation with Devpost search
✅ Documentation Q&A with RAG
✅ GitHub Progress Tracking
✅ Auto Pitch Deck Generation
✅ Real-time AI Chat
✅ Smart Fallback System
```

---

## 🔄 **Continuous Deployment**

After initial deployment, updates are automatic:

```bash
# Make changes
git add .
git commit -m "Add new feature"
git push

# Render and Vercel automatically deploy!
```

---

## 💰 **Cost Tracking**

| Service | Plan | Cost |
|---------|------|------|
| Render | Free | $0/month |
| Vercel | Hobby | $0/month |
| Elastic Cloud | Free Trial | $0 (14 days) |
| Google Cloud | Free Tier | $0 (with fallback) |
| **Total** | | **$0/month** |

---

## 🆘 **Common Issues**

### Issue: Backend build fails
**Solution**: 
```bash
# Test locally first
cd backend
pip install -r requirements.txt
python main.py
```

### Issue: Frontend build fails
**Solution**:
```bash
# Test locally first
cd frontend
npm run build
npm start
```

### Issue: CORS errors
**Solution**: Update backend `CORS_ORIGINS` environment variable

### Issue: 404 on API calls
**Solution**: Check `NEXT_PUBLIC_API_URL` includes `/api/v1`

### Issue: Render cold start (slow first request)
**Solution**: Normal for free tier (30 seconds). Use uptime monitor to keep warm.

---

## ✅ **Deployment Complete!**

When all checkboxes are checked, you have:
- ✅ Production-ready application
- ✅ Auto-deploying from GitHub
- ✅ Professional deployment setup
- ✅ Ready for hackathon submission
- ✅ Impressive for judges!

**Time to deploy**: ~10 minutes
**Ongoing cost**: $0
**Maintenance**: Automatic

**You're ready to win! 🏆**
