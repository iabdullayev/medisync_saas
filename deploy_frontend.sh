#!/bin/bash
set -e

# Configuration
REGION="us-east-1"
PROJECT_NAME="claimappeals"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${PROJECT_NAME}-frontend"

echo "🚀 Starting Frontend Deployment for MediSync SaaS..."

# 1. Login to ECR
echo "🔐 Authenticating with ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REPO

# 2. Build Image
echo "📦 Building Docker image..."
docker build -t $PROJECT_NAME-frontend .

# 3. Tag Image
echo "🏷️ Tagging image..."
docker tag $PROJECT_NAME-frontend:latest $ECR_REPO:latest

# 4. Push Image
echo "⬆️ Pushing to ECR..."
docker push $ECR_REPO:latest

# 5. Deploy Infrastructure
echo "☁️ Deploying with Terraform..."
cd infra

# Check if a failed service exists and delete it to prevent "already exists" errors
echo "🧹 Checking for failed service instances..."
FAILED_ARN=$(aws apprunner list-services --no-cli-pager --query "ServiceSummaryList[?ServiceName=='${PROJECT_NAME}-frontend' && Status=='CREATE_FAILED'].ServiceArn" --output text)
if [ ! -z "$FAILED_ARN" ]; then
    echo "⚠️ Found failed service: $FAILED_ARN. Deleting..."
    aws apprunner delete-service --no-cli-pager --service-arn $FAILED_ARN
    echo "⏳ Waiting for deletion to process..."
    sleep 30
fi

# Wait for service to be stable if it's already created/updating
echo "⏳ Waiting for App Runner service to be stable (RUNNING)..."
SERVICE_ARN=$(aws apprunner list-services --no-cli-pager --query "ServiceSummaryList[?ServiceName=='${PROJECT_NAME}-frontend'].ServiceArn" --output text)
if [ ! -z "$SERVICE_ARN" ]; then
    while true; do
        STATUS=$(aws apprunner describe-service --service-arn $SERVICE_ARN --no-cli-pager --query "Service.Status" --output text)
        echo "   Current Status: $STATUS"
        if [ "$STATUS" = "RUNNING" ]; then
            break
        fi
        sleep 20
    done
fi

# Step 5a: Target the domain association first (this pulls in the service and IAM role)
echo "🎯 Step 1: Initiating App Runner and Domain Association..."
terraform apply -target=aws_apprunner_custom_domain_association.domain -auto-approve

# Step 5b: Full apply to create DNS validation records
echo "🏁 Step 2: Finalizing DNS and Infrastructure..."
terraform apply -auto-approve

echo "✨ Deployment Complete!"
echo "🌐 Your app will be live at: https://denialcopilot.com"
echo "⏳ Note: DNS and SSL validation may take 15-30 minutes to propagate."
