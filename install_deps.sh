#!/bin/bash

echo "Installing dependencies..."
echo ""

# Install in batches
echo "1/3 Installing basic dependencies..."
python3 -m pip install --break-system-packages beautifulsoup4 feedparser requests python-dotenv pydantic

echo ""
echo "2/3 Installing AI/ML dependencies..."
python3 -m pip install --break-system-packages openai numpy

echo ""
echo "3/3 Installing vector DB and transformers..."
python3 -m pip install --break-system-packages chromadb sentence-transformers

echo ""
echo "All dependencies installed!"
echo ""
echo "Now you can run:"
echo "  ./run_app.sh"
