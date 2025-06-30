#!/bin/bash

# Docker run script for Image Captioning App

echo "🐳 Building and running Image Captioning App with Docker..."

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t image-captioning-app .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    # Run the container
    echo "🚀 Starting container..."
    docker run -d \
        --name image-captioning \
        -p 5000:5000 \
        -v $(pwd)/uploads:/app/uploads \
        -v $(pwd)/logs:/app/logs \
        image-captioning-app
    
    if [ $? -eq 0 ]; then
        echo "✅ Container started successfully!"
        echo "🌐 Application is running at: http://localhost:5000"
        echo "📊 Health check: http://localhost:5000/health"
        echo ""
        echo "📋 Useful commands:"
        echo "  - View logs: docker logs image-captioning"
        echo "  - Stop container: docker stop image-captioning"
        echo "  - Remove container: docker rm image-captioning"
    else
        echo "❌ Failed to start container"
        exit 1
    fi
else
    echo "❌ Failed to build Docker image"
    exit 1
fi 