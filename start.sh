#!/bin/bash

DB_FILE="/db/barbershop.db"

# Project setup script
echo "🚀 Starting project setup..."

# Check for Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is not installed. Please install it first."
    exit 1
fi

# Check for virtualenv
if ! command -v virtualenv &>/dev/null; then
    echo "⚠️ virtualenv not found. Installing it..."
    python3 -m pip install --user virtualenv
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if using SQLite, no migrations needed)
if [ ! -f "$DB_FILE" ]; then
    echo "🗄️ Setting up the database..."
    python -c "from package.models import Base, engine; Base.metadata.create_all(engine)"
fi

# Start FastAPI server
echo "🚀 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
