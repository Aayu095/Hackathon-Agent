@echo off
echo 🚀 Deploying Hackathon Agent to Google Cloud...

REM Check if gcloud is installed
gcloud --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Google Cloud CLI not found. Please install it first.
    echo https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Set project variables
set PROJECT_ID=hackathon-agent-2024
set REGION=us-central1
set SERVICE_NAME=hackathon-agent-api

echo 📋 Project: %PROJECT_ID%
echo 🌍 Region: %REGION%
echo 🔧 Service: %SERVICE_NAME%

REM Deploy backend to Cloud Run
echo.
echo 🔄 Deploying backend to Cloud Run...
cd backend

gcloud run deploy %SERVICE_NAME% ^
    --source . ^
    --platform managed ^
    --region %REGION% ^
    --project %PROJECT_ID% ^
    --allow-unauthenticated ^
    --memory 1Gi ^
    --cpu 1 ^
    --max-instances 10 ^
    --set-env-vars ENVIRONMENT=production,DEBUG=false

if %errorlevel% neq 0 (
    echo ❌ Backend deployment failed!
    pause
    exit /b 1
)

echo ✅ Backend deployed successfully!

REM Get the backend URL
for /f "tokens=*" %%i in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --project %PROJECT_ID% --format="value(status.url)"') do set BACKEND_URL=%%i

echo 🔗 Backend URL: %BACKEND_URL%

REM Deploy frontend to Vercel (or provide instructions)
cd ..\frontend

echo.
echo 📱 Frontend deployment options:
echo 1. Vercel (Recommended): vercel --prod
echo 2. Netlify: netlify deploy --prod
echo 3. Firebase Hosting: firebase deploy
echo.
echo 🔧 Set NEXT_PUBLIC_API_URL=%BACKEND_URL% in your frontend environment

echo.
echo ✅ Deployment completed!
echo 🌐 Backend: %BACKEND_URL%
echo 📚 API Docs: %BACKEND_URL%/api/v1/docs
echo.
pause
