#!/bin/bash

# Daily Decoy Upload Script
# Generates images, commits to GitHub, and uploads to TikTok

echo "=== Decoy Daily Upload ==="
echo ""

# Get today's date
TODAY=$(date +%Y-%m-%d)
IMAGE_DIR="generated_images/$TODAY"

# Step 1: Generate images
echo "Step 1: Generating images for $TODAY..."
python3 generate_images.py

if [ ! -d "$IMAGE_DIR" ]; then
    echo "Error: Images not generated. Check generate_images.py"
    exit 1
fi

echo "✓ Images generated"
echo ""

# Step 2: Commit and push to GitHub
echo "Step 2: Committing to GitHub..."
git add "$IMAGE_DIR"
git commit -m "Add daily deals for $TODAY

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push

echo "✓ Pushed to GitHub"
echo ""

# Wait a moment for GitHub to sync
echo "Waiting 5 seconds for GitHub to sync..."
sleep 5
echo ""

# Step 3: Upload to TikTok
echo "Step 3: Uploading to TikTok..."
python3 tiktok_uploader.py test

echo ""
echo "=== Complete ==="
echo "Check your TikTok inbox to review and publish the draft!"
