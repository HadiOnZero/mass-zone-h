#!/bin/bash

# Zone-H Mobile Mirror Tool Launcher
# Mobile Version with Kivy Framework
# Author: Hadi Ramdhani

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "📱 ZONE-H MOBILE MIRROR TOOL"
echo "============================="
echo "Mobile Version with Kivy Framework"
echo "Author: Hadi Ramdhani"
echo -e "${NC}"
echo ""

# Function to print colored output
print_status() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Python is installed
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    print_status "Please install Python 3.7+ first"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Python $PYTHON_VERSION is installed, but Python $REQUIRED_VERSION+ is required"
    exit 1
fi

print_success "Python $PYTHON_VERSION detected"

# Navigate to script directory
cd "$(dirname "$0")"

# Check if requirements file exists
if [ ! -f "requirements_mobile.txt" ]; then
    print_error "requirements_mobile.txt not found!"
    exit 1
fi

# Check if Kivy is installed
print_status "Checking dependencies..."
if ! python3 -c "import kivy" &> /dev/null; then
    print_warning "Kivy not found, installing dependencies..."
    
    # Try to install with pip3 first
    if command -v pip3 &> /dev/null; then
        print_status "Installing with pip3..."
        pip3 install -r requirements_mobile.txt
    elif command -v pip &> /dev/null; then
        print_status "Installing with pip..."
        pip install -r requirements_mobile.txt
    else
        print_error "pip not found! Please install pip first"
        exit 1
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
else
    print_success "Dependencies are already installed"
fi

# Check if main script exists
if [ ! -f "run_mobile.py" ]; then
    print_error "run_mobile.py not found!"
    exit 1
fi

# Start the mobile application
echo ""
print_status "Starting Zone-H Mobile Mirror..."
echo ""

# Set environment variables for better mobile experience
export KIVY_METRICS_DENSITY=1
export KIVY_METRICS_FONTSCALE=1

# Run the application
python3 run_mobile.py

echo ""
print_success "Application closed."
echo ""
print_status "Thank you for using Zone-H Mobile Mirror Tool!"
echo ""