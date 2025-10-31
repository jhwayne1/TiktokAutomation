# TikTok Integration Setup Guide

This guide walks you through setting up automated TikTok carousel uploads for Decoy Daily Deals.

## Prerequisites

1. TikTok Developer Account
2. Approved TikTok App with:
   - Client Key: `aw1n1yw1i6thayv0`
   - Client Secret: `jRlk9x6KxI5NF9Epfl5sfNyllLr7KJZP`
3. Domain verification complete for `www.decoys.me`
4. Images committed and pushed to GitHub (so they're publicly accessible)

## Setup Steps

### 1. Install Dependencies

```bash
pip install requests
```

### 2. First-Time Authorization

Run the authorization flow to connect your TikTok account:

```bash
python tiktok_uploader.py auth
```

This will:
- Open your browser to TikTok's authorization page
- Ask you to log in and authorize the app
- Prompt you to paste the redirect URL
- Save your access token to `tiktok_token.json`

**Important:** After authorizing, copy the FULL URL from your browser:
```
https://www.decoys.me/?code=XXXXXXXXXXXXX&state=decoy_upload
```

### 3. Test Upload

Once authorized, test with today's images:

```bash
python tiktok_uploader.py test
```

This will:
- Find today's images in `generated_images/YYYY-MM-DD/`
- Load the caption from `caption.txt`
- Upload carousel in order: cover → products → end page
- Create a draft in your TikTok inbox

## How It Works

### Image Upload Process

1. **Local Images**: Your generated images are stored in `generated_images/YYYY-MM-DD/`
2. **Public URLs**: Images are accessed via GitHub at:
   ```
   https://raw.githubusercontent.com/jhwayne1/TiktokAutomation/main/generated_images/YYYY-MM-DD/filename.png
   ```
3. **TikTok Upload**: The script uses TikTok's Content Posting API to create a photo carousel

### Carousel Order

The upload script arranges images in this order:
1. `cover_page.png` (first slide)
2. Individual product images (sorted alphabetically)
3. `end_page.png` (last slide with "link in bio")

### Upload Modes

**MEDIA_UPLOAD (default)**: Uploads to your TikTok inbox as a draft
- Allows you to review and edit before posting
- Posts are private until you publish them
- Recommended for daily workflow

**DIRECT_POST**: Posts immediately to your profile
- Requires additional permissions
- Posts go live immediately
- Use with caution

## Daily Workflow

### Step 1: Generate Images
```bash
python generate_images.py
```

### Step 2: Commit to GitHub
```bash
git add generated_images/YYYY-MM-DD/
git commit -m "Add daily deals for YYYY-MM-DD"
git push
```

### Step 3: Upload to TikTok
```bash
python tiktok_uploader.py test
```

### Step 4: Review & Publish
1. Open TikTok app on your phone
2. Check your Creator inbox
3. Review the draft
4. Add any final touches (music, effects)
5. Publish!

## Troubleshooting

### "No access token found"
Run `python tiktok_uploader.py auth` to authorize

### "Access token expired"
The script will automatically refresh the token using your refresh token

### "Images not found"
Make sure you've:
1. Generated images for today
2. Committed and pushed to GitHub
3. Waited a few seconds for GitHub to sync

### "TikTok API error"
Check:
- Your app is approved and not in sandbox mode
- Domain verification is complete
- Scopes include `video.publish`
- Images are publicly accessible

### "URL not accessible"
TikTok needs to access your images. Ensure:
- Images are committed to GitHub
- GitHub repository is public
- URLs follow format: `https://raw.githubusercontent.com/jhwayne1/TiktokAutomation/main/...`

## API Rate Limits

- **6 uploads per minute** per user access token
- Daily uploads should not hit this limit
- If you need to upload multiple times, wait 10 seconds between uploads

## Token Management

Tokens are stored in `tiktok_token.json`:
```json
{
  "data": {
    "access_token": "...",
    "refresh_token": "...",
    "expires_in": 86400,
    "token_type": "Bearer"
  }
}
```

**Security:**
- This file contains sensitive credentials
- It's in `.gitignore` and won't be committed
- Keep it secure and don't share it

## Advanced: Direct Posting

To post directly without drafts:

```python
upload_images_to_tiktok(carousel_images, caption, today, mode="DIRECT_POST")
```

**Note:** Direct posting:
- Requires app approval beyond sandbox
- Posts go live immediately
- Cannot be reviewed before publishing
- Recommended only after testing thoroughly

## Next Steps

1. Complete domain verification for TikTok
2. Run authorization: `python tiktok_uploader.py auth`
3. Test with sample upload: `python tiktok_uploader.py test`
4. Review draft in TikTok app
5. Publish if everything looks good!

## Support

For issues with:
- **TikTok API**: Check TikTok Developer Portal
- **Image generation**: See main README.md
- **Script errors**: Check error messages and ensure dependencies are installed
