#!/bin/bash

# Simple script to run the Gradio app

echo "Starting Deal Discovery System with Gradio..."
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "Python version: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" == "3.14" ]]; then
    echo "Warning: Python 3.14 detected. Some packages may have compatibility issues."
    echo "Consider using Python 3.11 or 3.12 for best compatibility."
    echo ""
fi

# Check if gradio is installed
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "Installing Gradio..."
    python3 -m pip install --break-system-packages gradio
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Ollama is not running!"
    echo "Please start it with: ollama serve"
    exit 1
fi

echo "Ollama is running"
echo "Starting Gradio app..."
echo ""
echo "Open your browser at: http://localhost:7860"
echo ""

cd "$(dirname "$0")"
python3 app.py
