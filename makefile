# Setup
IMAGE_NAME_API = voice-text-app/backend
IMAGE_NAME_WEB = voice-text-app/frontend

TAG = 1.0.0
REGION = ap-southeast-1
ACCOUNT_ID = 130506138320
ECR_REGISTRY = $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
ECR_IMAGE = $(ECR_REGISTRY)/$(IMAGE_NAME_API):$(TAG)

# Build Docker image
build-backend:
	docker build -t $(IMAGE_NAME_API):$(TAG) ./backend

build-frontend:
	docker build -t $(IMAGE_NAME_WEB):$(TAG) ./frontend

# # Push Docker image to ECR
# push-frontend: login build-frontend
# 	docker tag $(IMAGE_NAME_WEB):$(TAG) $(ECR_REGISTRY)/$(IMAGE_NAME_WEB):$(TAG)
# 	docker push $(ECR_REGISTRY)/$(IMAGE_NAME_WEB):$(TAG)

# push-backend: login build-backend
# 	docker tag $(IMAGE_NAME_API):$(TAG) $(ECR_REGISTRY)/$(IMAGE_NAME_API):$(TAG)
# 	docker push $(ECR_REGISTRY)/$(IMAGE_NAME_API):$(TAG)

build: build-frontend build-backend

# push: push-frontend push-backend

run:
	docker compose up -d -V

down:
	docker compose down --volumes


# Login ECR
login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ECR_REGISTRY)

# Logout ECR
logout:
	docker logout $(ECR_REGISTRY)