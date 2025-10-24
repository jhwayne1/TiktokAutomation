# GitHub Actions Setup Guide

This guide will help you set up automated daily image generation using GitHub Actions.

## Prerequisites

- A GitHub account (you have: https://github.com/jhwayne1)
- Git installed on your computer

## Setup Steps

### 1. Create a New GitHub Repository

1. Go to https://github.com/new
2. Repository name: `TiktokAutomation` (or any name you prefer)
3. Description: "Automated TikTok daily deals image generator"
4. Choose **Public** or **Private** (both work)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 2. Push Your Code to GitHub

Open Terminal and navigate to your project folder:

```bash
cd /Users/jakewayne/Desktop/TiktokAutomation

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: TikTok automation system"

# Add your GitHub repository as remote (replace with your actual repo URL)
git remote add origin https://github.com/jhwayne1/TiktokAutomation.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Verify GitHub Actions Workflow

1. Go to your repository on GitHub: `https://github.com/jhwayne1/TiktokAutomation`
2. Click on the "Actions" tab
3. You should see the workflow "Generate Daily TikTok Images"
4. The workflow is now set to run automatically at 7:00 AM EST every day

### 4. Test the Workflow Manually (Recommended)

Before waiting until 7 AM tomorrow, test it now:

1. Go to the "Actions" tab in your repository
2. Click on "Generate Daily TikTok Images" workflow
3. Click "Run workflow" button (top right)
4. Select branch "main"
5. Click "Run workflow"

The workflow will run and you can watch the progress in real-time!

### 5. Access Generated Images

After the workflow completes, you can access images in two ways:

#### Option A: Download from Artifacts
1. Go to the workflow run that completed
2. Scroll down to "Artifacts" section
3. Download the `tiktok-images-YYYY-MM-DD.zip` file
4. Unzip to access all generated images

#### Option B: View in Repository (if auto-commit is enabled)
1. The images will be committed to the `generated_images/YYYY-MM-DD/` folder
2. Browse them directly in your repository
3. Download individual files as needed

## Important Notes

### Timezone Configuration

The workflow is currently set to run at **7:00 AM EST (12:00 PM UTC)**.

To change the time, edit `.github/workflows/generate-daily-images.yml`:

```yaml
schedule:
  # Current: 7 AM EST = 12 PM UTC
  - cron: '0 12 * * *'

  # For different times, use: 'minute hour * * *'
  # Examples:
  # 6 AM EST (11 AM UTC): '0 11 * * *'
  # 8 AM EST (1 PM UTC):  '0 13 * * *'
  # 7 AM PST (3 PM UTC):  '0 15 * * *'
```

### Storage Considerations

**Artifacts (Default Method):**
- ✅ Images available for 30 days
- ✅ No repository bloat
- ✅ Easy to download
- ❌ Automatically deleted after 30 days

**Auto-commit (Optional):**
- ✅ Images permanently stored in repo
- ✅ Version history of all images
- ✅ Easy to browse
- ❌ Repository size grows over time
- ❌ May hit GitHub size limits eventually

The workflow currently uses **both methods** - you get artifacts for easy download, and optionally commits to the repo.

To **disable auto-commit**, edit `.github/workflows/generate-daily-images.yml` and remove or comment out the last step:

```yaml
# Comment out or remove this entire section:
# - name: Commit and push images (optional)
#   run: |
#     ...
```

## Notifications

### Get Notified When Images Are Ready

1. Go to your repository settings
2. Navigate to "Notifications"
3. Or watch the repository:
   - Click "Watch" at the top of your repository
   - Choose "Custom" → Check "Workflows"

GitHub will email you when workflows complete (or fail).

### Slack/Discord Notifications (Advanced)

You can add Slack or Discord notifications to the workflow. Let me know if you want to set this up!

## Troubleshooting

### Workflow Doesn't Run
- Check the "Actions" tab → ensure Actions are enabled
- Verify the cron schedule is correct for your timezone
- GitHub Actions may have a slight delay (up to 15 minutes)

### Workflow Fails
- Click on the failed workflow run
- Expand each step to see error messages
- Common issues:
  - API rate limits
  - Network timeouts
  - Out of memory (rare)

### Manual Trigger Doesn't Show Up
- Ensure you've pushed the `.github/workflows/generate-daily-images.yml` file
- Refresh the Actions page
- Check that the file is in the correct location

## Cost

GitHub Actions is **FREE** for:
- Public repositories: Unlimited
- Private repositories: 2,000 minutes/month

Your workflow takes about 5-10 minutes to run, so you get ~200-400 runs/month for free on private repos.

## Next Steps

1. Push your code to GitHub (see Step 2 above)
2. Run a test workflow to verify everything works
3. Wait until tomorrow at 7 AM to see automatic generation!
4. Download your images and post to TikTok

## Support

If you encounter any issues:
1. Check the workflow logs in the Actions tab
2. Ensure all files are committed and pushed
3. Verify the API endpoint is accessible

---

**Ready to get started?** Follow Step 1 above to create your repository!
