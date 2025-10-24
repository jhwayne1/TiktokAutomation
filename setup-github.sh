#!/bin/bash

echo "=========================================="
echo "GitHub Repository Setup Script"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   Visit: https://git-scm.com/downloads"
    exit 1
fi

echo "✓ Git is installed"
echo ""

# Get repository URL from user
echo "Please enter your GitHub repository URL:"
echo "(Example: https://github.com/jhwayne1/TiktokAutomation.git)"
read -p "Repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No repository URL provided. Exiting."
    exit 1
fi

echo ""
echo "Setting up repository..."
echo ""

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "→ Initializing Git repository..."
    git init
else
    echo "→ Git repository already initialized"
fi

# Add all files
echo "→ Adding files to Git..."
git add .

# Commit
echo "→ Creating initial commit..."
git commit -m "Initial commit: TikTok automation system with GitHub Actions" || echo "  (No changes to commit)"

# Add remote
echo "→ Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

# Set branch to main
echo "→ Setting branch to main..."
git branch -M main

# Push to GitHub
echo "→ Pushing to GitHub..."
git push -u origin main

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Visit your repository: ${REPO_URL%.git}"
echo "2. Go to the 'Actions' tab"
echo "3. Click 'Run workflow' to test the automation"
echo ""
echo "Your images will be generated automatically every day at 7:00 AM EST!"
echo ""
