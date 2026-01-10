#!/bin/bash

# Quick startup script for Linux/macOS
# AI Agent Conversational Application

echo ""
echo "================================"
echo "  AI Agent - Startup Script"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

python3 --version
echo "[OK] Python found"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found"
    echo "Please create .env file with your OpenAI API key:"
    echo "  OPENAI_API_KEY=sk-proj-xxxxx"
    echo ""
fi

# Install dependencies
echo "[INFO] Checking dependencies..."
pip3 install -q openai python-dotenv

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo "[OK] Dependencies ready"

# Launch the application
echo "[INFO] Starting AI Agent..."
echo ""
python3 main.py
