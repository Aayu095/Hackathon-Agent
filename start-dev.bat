@echo off
echo 🤖 Starting Hackathon Agent Development Environment...

REM Check if .env files exist
if not exist "backend\.env" (
    echo 📝 Creating backend .env file from example...
    copy "backend\.env.example" "backend\.env"
)

if not exist "frontend\.env.local" (
    echo 📝 Creating frontend .env.local file from example...
    copy "frontend\.env.local.example" "frontend\.env.local"
)

echo.
echo 🔧 Setting up Python virtual environment...
cd backend
if not exist "venv" (
    python -m venv venv
)

echo 📦 Installing backend dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo 🔧 Setting up Elasticsearch indices and sample data...
python scripts\quick_setup.py

echo.
echo 🚀 Starting backend server on port 8000...
start cmd /k "cd /d %cd% && venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

cd ..\frontend

echo 📦 Installing frontend dependencies...
call npm install

REM Wait for backend to start
echo ⏳ Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

echo 🚀 Starting frontend server on port 3000...
start cmd /k "cd /d %cd% && npm run dev"

echo.
echo ✅ Both servers are starting...
echo 🔗 Backend API: http://localhost:8000
echo 🌐 Frontend UI: http://localhost:3000  
echo 📚 API Documentation: http://localhost:8000/api/v1/docs
echo 💬 Chat Interface: http://localhost:3000
echo.
echo 🎯 Ready for hackathon development!
pause
