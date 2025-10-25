#!/bin/bash

# AI-Powered Hackathon Agent - Deployment Script
# Deploy to Google Cloud Run

set -e

echo "🚀 Deploying AI-Powered Hackathon Agent to Google Cloud Run..."

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
REGION=${REGION:-"us-central1"}
BACKEND_SERVICE_NAME="hackathon-agent-api"
FRONTEND_SERVICE_NAME="hackathon-agent-frontend"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo_error "gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo_error "Please authenticate with gcloud: gcloud auth login"
    exit 1
fi

# Set project
echo_info "Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo_info "Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Deploy Backend
echo_info "Deploying backend service..."
cd backend

gcloud run deploy $BACKEND_SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --set-env-vars "ENVIRONMENT=production,DEBUG=false" \
    --timeout 300

# Get backend URL
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE_NAME --region $REGION --format 'value(status.url)')
echo_info "Backend deployed at: $BACKEND_URL"

cd ..

# Deploy Frontend
echo_info "Deploying frontend service..."
cd frontend

# Set backend URL for frontend
export NEXT_PUBLIC_API_URL=$BACKEND_URL

gcloud run deploy $FRONTEND_SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 5 \
    --set-env-vars "NEXT_PUBLIC_API_URL=$BACKEND_URL" \
    --timeout 300

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE_NAME --region $REGION --format 'value(status.url)')
echo_info "Frontend deployed at: $FRONTEND_URL"

cd ..

echo_info "✅ Deployment completed successfully!"
echo_info "🌐 Frontend: $FRONTEND_URL"
echo_info "🔧 Backend API: $BACKEND_URL"
echo_info "📚 API Docs: $BACKEND_URL/api/v1/docs"

echo_warn "⚠️  Don't forget to:"
echo_warn "   1. Set up your Elastic Cloud credentials"
echo_warn "   2. Configure Google Cloud service account"
echo_warn "   3. Set up GitHub webhook URL: $BACKEND_URL/api/v1/github/webhook"
echo_warn "   4. Update CORS origins in backend configuration"
