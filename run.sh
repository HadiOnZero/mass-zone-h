#!/bin/bash

# Zone-H Mass Mirror Launcher Script
# For Linux/Mac systems

echo "🎯 Zone-H Mass Mirror Tool"
echo "=========================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.6 or higher"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    echo "Please install pip3"
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet
    echo "✅ Dependencies installed/updated"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    exit 1
fi

echo ""
echo "🚀 Starting Zone-H Mass Mirror Tool..."
echo "====================================="
echo ""

# Run the application
python3 main.py