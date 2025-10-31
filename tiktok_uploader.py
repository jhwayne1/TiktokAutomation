"""
TikTok Content Posting API Integration
Automatically uploads generated carousel images to TikTok as drafts
"""

import os
import json
import time
import requests
from urllib.parse import urlencode
import webbrowser
from datetime import datetime

# TikTok API credentials (Sandbox)
CLIENT_KEY = "sbawefp9sckxkckw6x"
CLIENT_SECRET = "Edpgors7PlmNJrK1ZhKywc5jTsu619xl"
REDIRECT_URI = "https://www.decoys.me/"  # Must match what you set in TikTok Developer Portal

# TikTok API endpoints
AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
PHOTO_UPLOAD_URL = "https://open.tiktokapis.com/v2/post/publish/content/init/"

# File to store access token
TOKEN_FILE = "tiktok_token.json"


def get_authorization_url():
    """Generate the OAuth authorization URL"""
    params = {
        'client_key': CLIENT_KEY,
        'scope': 'user.info.basic,video.upload',
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': 'decoy_upload'
    }

    url = f"{AUTH_URL}?{urlencode(params)}"
    return url


def get_access_token(auth_code):
    """Exchange authorization code for access token"""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache'
    }

    data = {
        'client_key': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()

    token_data = response.json()

    # Save token to file
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print("✓ Access token saved successfully!")
    return token_data


def load_token():
    """Load saved access token"""
    if not os.path.exists(TOKEN_FILE):
        return None

    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)


def refresh_access_token(refresh_token):
    """Refresh the access token using refresh token"""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache'
    }

    data = {
        'client_key': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()

    token_data = response.json()

    # Save new token
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print("✓ Access token refreshed!")
    return token_data


def authorize():
    """Start OAuth flow to get authorization"""
    print("\n=== TikTok Authorization ===")
    print("\nStep 1: Opening browser for authorization...")
    print("Please log in to TikTok and authorize the app.")

    auth_url = get_authorization_url()
    print(f"\nAuthorization URL:\n{auth_url}\n")

    # Open browser
    webbrowser.open(auth_url)

    print("\nAfter authorizing, you'll be redirected to your redirect URI.")
    print("Copy the FULL URL from your browser's address bar.")
    print("It will look like: https://www.decoys.me/?code=XXXXX&state=decoy_upload\n")

    redirect_url = input("Paste the full redirect URL here: ").strip()

    # Extract authorization code from URL
    if '?code=' in redirect_url:
        auth_code = redirect_url.split('?code=')[1].split('&')[0]
    elif 'code=' in redirect_url:
        auth_code = redirect_url.split('code=')[1].split('&')[0]
    else:
        raise ValueError("Could not find authorization code in URL")

    print(f"\n✓ Authorization code received: {auth_code[:20]}...")

    # Exchange for access token
    print("\nStep 2: Exchanging code for access token...")
    token_data = get_access_token(auth_code)

    print("\n✓ Authorization complete!")
    print(f"Access token: {token_data.get('data', {}).get('access_token', '')[:20]}...")

    return token_data


def upload_images_to_github(image_paths, date_folder):
    """
    Upload images to GitHub to make them publicly accessible for TikTok

    Args:
        image_paths: List of local image file paths
        date_folder: Date folder (e.g., '2025-10-30')

    Returns:
        List of public GitHub URLs for the images
    """
    print(f"\n=== Preparing Images ===")
    print("Images need to be publicly accessible for TikTok API")
    print(f"Images are already in: generated_images/{date_folder}")

    # Images should already be in git repo
    # After commit/push, they'll be available at:
    # https://raw.githubusercontent.com/jhwayne1/TiktokAutomation/main/generated_images/{date_folder}/{filename}

    github_urls = []
    for img_path in image_paths:
        filename = os.path.basename(img_path)
        github_url = f"https://raw.githubusercontent.com/jhwayne1/TiktokAutomation/main/generated_images/{date_folder}/{filename}"
        github_urls.append(github_url)
        print(f"  {filename} -> GitHub")

    return github_urls


def upload_images_to_tiktok(image_paths, caption, date_folder, mode="MEDIA_UPLOAD"):
    """
    Upload images as a carousel post to TikTok

    Args:
        image_paths: List of image file paths (local paths)
        caption: Caption text for the post
        date_folder: Date folder (e.g., '2025-10-30')
        mode: "MEDIA_UPLOAD" for drafts or "DIRECT_POST" for immediate posting
    """
    print(f"\n=== Uploading to TikTok ===")
    print(f"Date: {date_folder}")
    print(f"Images: {len(image_paths)}")
    print(f"Caption: {caption[:50]}...")
    print(f"Mode: {mode}")

    # Load or get access token
    token_data = load_token()

    if not token_data:
        print("\n⚠ No access token found. Starting authorization flow...")
        token_data = authorize()

    access_token = token_data.get('data', {}).get('access_token')

    if not access_token:
        raise ValueError("No access token available. Please run authorization first.")

    # Convert local paths to public GitHub URLs
    print("\nStep 1: Generating public URLs for images...")
    photo_urls = upload_images_to_github(image_paths, date_folder)

    print(f"\n✓ Generated {len(photo_urls)} public URLs")

    # Prepare API request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    # Build request body according to TikTok API spec
    request_body = {
        "media_type": "PHOTO",
        "post_mode": mode,
        "post_info": {
            "title": caption[:90],  # Max 90 characters for title
            "description": caption[:4000],  # Max 4000 characters
            "privacy_level": "SELF_ONLY" if mode == "MEDIA_UPLOAD" else "PUBLIC_TO_EVERYONE",
            "disable_comment": False,
            "auto_add_music": True,
            "brand_content_toggle": False,
            "brand_organic_toggle": True  # Using for own business (Decoy)
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "photo_images": photo_urls,
            "photo_cover_index": 0  # First image as cover
        }
    }

    print("\nStep 2: Uploading to TikTok...")
    print(f"Endpoint: {PHOTO_UPLOAD_URL}")
    print(f"Photos: {len(photo_urls)}")

    try:
        response = requests.post(
            PHOTO_UPLOAD_URL,
            headers=headers,
            json=request_body,
            timeout=30
        )

        print(f"\nResponse Status: {response.status_code}")
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")

        if response.status_code == 200:
            if response_data.get('error', {}).get('code') == 'ok':
                print("\n✓ SUCCESS! Carousel uploaded to TikTok!")

                if mode == "MEDIA_UPLOAD":
                    print("✓ Check your TikTok inbox for the uploaded draft")
                else:
                    print("✓ Post published to your TikTok profile")

                return True
            else:
                print(f"\n⚠ Upload failed: {response_data.get('error', {}).get('message')}")
                return False
        else:
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error uploading to TikTok: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

    return True


def main():
    """Main function to handle TikTok uploads"""
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == 'auth':
            # Run authorization flow
            authorize()
            return
        elif sys.argv[1] == 'test':
            # Test with today's images
            today = datetime.now().strftime('%Y-%m-%d')
            image_folder = f'generated_images/{today}'

            if not os.path.exists(image_folder):
                print(f"⚠ Folder not found: {image_folder}")
                return

            # Get carousel images in order: cover, products, end
            cover_page = os.path.join(image_folder, 'cover_page.png')
            end_page = os.path.join(image_folder, 'end_page.png')

            # Get product images (exclude cover and end)
            product_images = sorted([
                os.path.join(image_folder, f)
                for f in os.listdir(image_folder)
                if f.endswith('.png') and f not in ['cover_page.png', 'end_page.png']
            ])

            # Build carousel: cover + products + end
            carousel_images = []
            if os.path.exists(cover_page):
                carousel_images.append(cover_page)

            carousel_images.extend(product_images)

            if os.path.exists(end_page):
                carousel_images.append(end_page)

            # Load caption
            caption_file = os.path.join(image_folder, 'caption.txt')
            if os.path.exists(caption_file):
                with open(caption_file, 'r') as f:
                    caption = f.read().strip()
            else:
                caption = "Daily deals! Check link in bio 🛍️"

            print(f"\n=== Test Upload ===")
            print(f"Found {len(carousel_images)} images in {image_folder}")
            print(f"  - Cover page: {'✓' if os.path.exists(cover_page) else '✗'}")
            print(f"  - Product images: {len(product_images)}")
            print(f"  - End page: {'✓' if os.path.exists(end_page) else '✗'}")
            print(f"Caption: {caption[:100]}...")

            upload_images_to_tiktok(carousel_images, caption, today)
    else:
        print("\n=== TikTok Uploader ===")
        print("\nUsage:")
        print("  python tiktok_uploader.py auth     - Authorize with TikTok")
        print("  python tiktok_uploader.py test     - Test upload with today's images")
        print("\nFirst run: python tiktok_uploader.py auth")


if __name__ == "__main__":
    main()
