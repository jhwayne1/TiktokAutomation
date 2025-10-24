# Quick Start Guide

Get your TikTok automation running in 5 minutes!

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `TiktokAutomation`
3. Choose Public or Private
4. Click "Create repository"
5. **COPY** the repository URL (e.g., `https://github.com/jhwayne1/TiktokAutomation.git`)

## Step 2: Run Setup Script

Open Terminal and run:

```bash
cd /Users/jakewayne/Desktop/TiktokAutomation
./setup-github.sh
```

Paste your repository URL when prompted.

## Step 3: Test the Workflow

1. Visit your repository on GitHub
2. Click the **"Actions"** tab
3. Select **"Generate Daily TikTok Images"**
4. Click **"Run workflow"** → Select "main" → Click **"Run workflow"**
5. Watch it run! (takes 5-10 minutes)

## Step 4: Download Your Images

After the workflow completes:

1. Scroll down to **"Artifacts"** section
2. Download `tiktok-images-YYYY-MM-DD.zip`
3. Unzip and post to TikTok!

## Done! 🎉

Your images will now generate automatically every morning at 7:00 AM EST.

---

## Troubleshooting

**"Permission denied" when running setup-github.sh**
```bash
chmod +x setup-github.sh
./setup-github.sh
```

**"Actions tab not showing workflow"**
- Wait 30 seconds and refresh
- Check that files are in `.github/workflows/` folder

**"Workflow failed"**
- Click on the failed workflow
- Expand the steps to see the error
- Most common: API rate limiting (wait and try again)

---

## Daily Routine

1. **Wake up at 7 AM** ☕
2. **Check GitHub Actions** (or wait for notification)
3. **Download images from Artifacts**
4. **Post to TikTok** 🚀

That's it!

---

For detailed documentation, see:
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - Complete setup guide
- [README.md](README.md) - Full documentation
