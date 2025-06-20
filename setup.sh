#!/bin/bash
set -e

# 1. Check if python 3.12, 3.11 or 3.10 already exist
if command -v python3.12 &> /dev/null; then
    echo "✅ Python 3.12 is already installed"
    PYTHON_CMD="python3.12"
elif command -v python3.11 &> /dev/null; then
    echo "✅ Python 3.11 is already installed"
    PYTHON_CMD="python3.11"
elif command -v python3.10 &> /dev/null; then
    echo "✅ Python 3.10 is already installed"
    PYTHON_CMD="python3.10"

# 1. Ask for permission to install Python 3.12 if not already installed
else
    read -p "💡 Can I install Python 3.12? (y/n): " answer
    if [[ ! "$answer" =~ ^[Yy](es)?$ ]]; then
        echo "❌ Installation cancelled by user"
        exit 0
    fi
    
    # Detect operating system and install Python 3.12
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install -y python3.12 python3.12-venv python3.12-dev
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python@3.12
    else
        echo "❌ Unsupported operating system: $OSTYPE"
        exit 1
    fi
    echo "✅ Python 3.12 has been installed"
    PYTHON_CMD="python3.12"
fi

# 2. Ask for permission to make Python virtual environment
read -p "💡 Can I create a Python virtual environment? (y/n): " answer
if [[ ! "$answer" =~ ^[Yy](es)?$ ]]; then
    echo "❌ Virtual environment creation cancelled by user"
    exit 0
fi
$PYTHON_CMD -m venv pdfmcp
source pdfmcp/bin/activate
echo "✅ Python virtual environment has been created"

# 3. Ask for permission to install masquerade
read -p "💡 Can I install Masquerade (this github repository)? (y/n): " answer
if [[ ! "$answer" =~ ^[Yy](es)?$ ]]; then
    echo "❌ Masquerade installation cancelled by user"
    exit 0
fi
pip install git+https://github.com/postralai/masquerade@main
echo "✅ Masquerade has been installed"

# Configure masquerade
python -m masquerade.configure_claude