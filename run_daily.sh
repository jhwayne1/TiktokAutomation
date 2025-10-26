#!/bin/bash
# Daily TikTok Image Generator - Run this script locally each day

echo "========================================"
echo "TikTok Daily Image Generator"
echo "========================================"
echo ""

# Activate virtual environment
source venv/bin/activate

# Generate all images
echo "Generating images for today's deals..."
python3 generate_all_images.py

echo ""
echo "Generating caption..."
python3 generate_caption.py

echo ""
echo "========================================"
echo "Done! Check the generated_images folder"
echo "========================================"
