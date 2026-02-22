#!/bin/bash

# Deployment script for Docker Intelligence Generator

echo "🚀 Deploying Docker Intelligence Generator..."
echo ""

# Stop existing container
echo "📦 Stopping existing container..."
docker-compose down

# Build new image
echo "🔨 Building Docker image..."
docker-compose build

# Start container
echo "▶️  Starting container..."
docker-compose up -d

# Wait for health check
echo "⏳ Waiting for application to be healthy..."
sleep 10

# Check status
echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access the application at: http://localhost:4000"
echo "📋 View logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down"
