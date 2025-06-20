#!/bin/bash
set -e

# Check if python3.12 already exists
if command -v python3.12 &> /dev/null; then
    echo "✅ Python 3.12 is already installed"
else
    # Ask for permission to install Python 3.12
    read -p "💡 Can I install Python 3.12? (y/n): " answer
    
    # Check if answer is yes (case insensitive)
    if [[ ! "$answer" =~ ^[Yy](es)?$ ]]; then
        echo "❌ Installation cancelled by user."
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
fi

python3.12 -m venv pdfmcp
source pdfmcp/bin/activate
pip install git+https://github.com/postralai/masquerade@main
python -m masquerade.configure_claude