# Image Captioning App - Docker Setup

This document explains how to run the Image Captioning application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier management)

## Quick Start

### Option 1: Using the provided script (Recommended)

```bash
# Make the script executable (if not already done)
chmod +x docker-run.sh

# Run the application
./docker-run.sh
```

### Option 2: Using Docker Compose

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 3: Manual Docker commands

```bash
# Build the Docker image
docker build -t image-captioning-app .

# Run the container
docker run -d \
    --name image-captioning \
    -p 5000:5000 \
    -v $(pwd)/uploads:/app/uploads \
    -v $(pwd)/logs:/app/logs \
    image-captioning-app
```

## Accessing the Application

Once the container is running, you can access the application at:
- **Main Application**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## Container Management

### View logs
```bash
# Using Docker
docker logs image-captioning

# Using Docker Compose
docker-compose logs -f
```

### Stop the container
```bash
# Using Docker
docker stop image-captioning

# Using Docker Compose
docker-compose down
```

### Remove the container
```bash
# Using Docker
docker rm image-captioning

# Using Docker Compose
docker-compose down --rmi all
```

### Restart the container
```bash
# Using Docker
docker restart image-captioning

# Using Docker Compose
docker-compose restart
```

## Volume Mounts

The application uses the following volume mounts:
- `./uploads:/app/uploads` - For storing uploaded images
- `./logs:/app/logs` - For application logs

## Environment Variables

The following environment variables are set in the container:
- `FLASK_APP=app.py`
- `FLASK_ENV=production`
- `PYTHONUNBUFFERED=1`

## Health Check

The container includes a health check that monitors the application status:
- Checks every 30 seconds
- Timeout of 10 seconds
- Retries 3 times before marking as unhealthy

## Troubleshooting

### Container won't start
1. Check if port 5000 is already in use:
   ```bash
   lsof -i :5000
   ```
2. View container logs:
   ```bash
   docker logs image-captioning
   ```

### Models not loading
1. Ensure the `models/` directory contains:
   - `model.keras`
   - `tokenizer.pkl`
   - `feature_extractor.keras`

### Permission issues
1. Check file permissions:
   ```bash
   ls -la uploads/ logs/
   ```
2. Fix permissions if needed:
   ```bash
   chmod 755 uploads/ logs/
   ```

### Memory issues
If the container runs out of memory, you can increase the memory limit:
```bash
docker run -d \
    --name image-captioning \
    --memory=4g \
    -p 5000:5000 \
    -v $(pwd)/uploads:/app/uploads \
    -v $(pwd)/logs:/app/logs \
    image-captioning-app
```

## Development

For development, you can run the container with debug mode:
```bash
docker run -d \
    --name image-captioning-dev \
    -p 5000:5000 \
    -v $(pwd):/app \
    -e FLASK_ENV=development \
    image-captioning-app
```

## Security Notes

- The application runs as a non-root user inside the container
- File uploads are limited to 16MB
- Only image files are accepted
- Uploaded files are automatically cleaned up after processing 