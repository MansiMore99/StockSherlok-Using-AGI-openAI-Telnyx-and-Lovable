#!/bin/bash

# StockSherlok Quick Start Script

echo "================================================"
echo "🔍 StockSherlok - Quick Start Setup"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo ""
echo "Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

if ! command_exists pip3; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi
echo "✅ pip3 found"

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi
echo "✅ npm found: $(npm --version)"

# Setup backend
echo ""
echo "================================================"
echo "Setting up backend..."
echo "================================================"

cd backend || exit 1

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - TELNYX_API_KEY (optional)"
    echo "   - TELNYX_PHONE_NUMBER (optional)"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

cd ..

# Setup frontend
echo ""
echo "================================================"
echo "Setting up frontend..."
echo "================================================"

cd frontend || exit 1

# Install Node dependencies
echo ""
echo "Installing Node.js dependencies (this may take a few minutes)..."
npm install

cd ..

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit backend/.env with your API keys"
echo ""
echo "2. Start the backend server:"
echo "   cd backend"
echo "   python3 app.py"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "For Docker deployment:"
echo "   docker-compose up -d"
echo ""
echo "================================================"
