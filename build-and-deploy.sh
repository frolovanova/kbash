#!/bin/bash

# Configuration
DOCKER_REPO="containers.stagingterritory.com/lab/bifrost"
IMAGE_TAG="latest"
DEPLOYMENT_NAME="lab"
NAMESPACE="lab"  # Change if your deployment is in a different namespace

# Build the Docker image
echo "Building Docker image..."
docker build -t ${DOCKER_REPO}:${IMAGE_TAG} .

# Push the Docker image to the registry
echo "Pushing Docker image to the registry..."
docker push ${DOCKER_REPO}:${IMAGE_TAG}

# Ensure the latest image is pulled by deleting the pod(s)
echo "Deleting existing pod(s) to pull the latest image..."
kubectl delete pod -l app=${DEPLOYMENT_NAME} -n ${NAMESPACE}

# Wait for the new pod(s) to be up and running
echo "Waiting for new pod(s) to be up and running..."
kubectl rollout status deployment/${DEPLOYMENT_NAME} -n ${NAMESPACE}

echo "Deployment completed successfully."

