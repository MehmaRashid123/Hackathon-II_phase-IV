#!/bin/bash

# Startup script for FastAPI Task API server

echo "🚀 Starting FastAPI Task API Server..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start server
echo "📡 Server starting on http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn src.main:app --reload --port 8000
