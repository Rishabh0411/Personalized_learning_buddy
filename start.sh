#!/bin/bash

# Quick start script for Personalized Learning Buddy
# This script sets up and runs the application

echo "🧠 Personalized Learning Buddy - Quick Start"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install requirements
echo "📦 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your OpenAI API key"
    echo "   Get your key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter to continue (or Ctrl+C to exit and add API key first)..."
fi

# Create sample data
echo "📝 Creating sample notes for testing..."
python create_sample_data.py

# Run tests
echo ""
echo "🧪 Running setup tests..."
python test_setup.py

echo ""
echo "=============================================="
echo "🚀 Starting the application..."
echo "=============================================="
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Streamlit app
streamlit run app.py
