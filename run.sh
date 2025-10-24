#!/bin/bash

# TikTok Image Generator Runner Script

echo "=================================="
echo "TikTok Image Asset Generator"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "Running image generator..."
echo ""

# Run the master generator (generates both individual images and cover page)
python generate_all_images.py

echo ""
echo "Done!"
