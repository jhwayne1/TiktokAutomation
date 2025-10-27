#!/usr/bin/env python3
"""
TikTok Cover Page Generator
Creates a collage-style cover page with today's deals
"""

import os
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from rembg import remove
import random
import math


# Configuration
API_URL = "https://item-api-rosy.vercel.app/api/deals"
LOGO_PATH = "DecoyWizard.png"
OUTPUT_BASE_DIR = "generated_images"
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920

# Asset paths
SPARKLE_EMOJI_PATH = "sparkle-emoji.png"
MONEY_STACK_PATH = "MoneyStack.png"
CREDIT_CARD_PATH = "CreditCard.png"
GIFT_PATH = "Gift.png"
DISCOUNT_SIGN_PATH = "discountsign.png"

# Font paths
FONT_PATHS_MEDIUM = [
    "/Library/Fonts/SF-Pro-Rounded-Medium.otf",
    "/System/Library/Fonts/SFProRounded-Medium.ttf",
    "/System/Library/Fonts/Supplemental/SF-Pro-Rounded-Medium.otf",
    "/System/Library/Fonts/SF-Pro-Medium.ttf",
]


def get_font_path(weight='medium'):
    """Find available SF Pro Rounded font with specified weight"""
    paths = FONT_PATHS_MEDIUM

    for path in paths:
        if os.path.exists(path):
            return path

    print("Warning: SF Pro Rounded Medium not found, using default font")
    return None


def create_gradient_background(width, height):
    """Create a gradient background from light blue to pink"""
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Define colors (light blue to pink)
    color_start = (190, 227, 248)  # Light blue
    color_end = (239, 198, 237)    # Light pink

    # Create vertical gradient
    for y in range(height):
        ratio = y / height
        r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
        g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
        b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return img


def fetch_deals():
    """Fetch deals from API"""
    print("Fetching deals from API...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('deals', [])
    except Exception as e:
        print(f"Error fetching deals: {e}")
        return []


def download_image(url):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None


def remove_background(image):
    """Remove background from image using rembg"""
    try:
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        output = remove(img_byte_arr.read())
        return Image.open(BytesIO(output))
    except Exception as e:
        print(f"  Error removing background: {e}")
        return image


def add_text_with_shadow(draw, text, position, font_size, font_path, fill='white', shadow_offset=4):
    """Add text with shadow effect"""
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()

        x, y = position

        # Draw shadow (slightly offset, darker)
        shadow_color = (180, 180, 180, 200)  # Light gray shadow
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)

        # Draw main text
        draw.text((x, y), text, font=font, fill=fill)

    except Exception as e:
        print(f"  Error adding text: {e}")


def create_cover_page(deals, font_path):
    """Create TikTok cover page with multiple products"""
    print("Creating cover page...")

    # Create gradient background
    canvas = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT)

    # Load and add logo at the top
    try:
        logo = Image.open(LOGO_PATH)
        logo_max_width = 350
        logo_ratio = logo_max_width / logo.width
        logo_height = int(logo.height * logo_ratio)
        logo = logo.resize((logo_max_width, logo_height), Image.Resampling.LANCZOS)

        logo_x = (IMAGE_WIDTH - logo_max_width) // 2
        logo_y = 60

        if logo.mode == 'RGBA':
            canvas.paste(logo, (logo_x, logo_y), logo)
        else:
            canvas.paste(logo, (logo_x, logo_y))

        current_y = logo_y + logo_height + 40
    except Exception as e:
        print(f"  Error loading logo: {e}")
        current_y = 100

    # Add "decoy daily deals" text with sparkles
    draw = ImageDraw.Draw(canvas, 'RGBA')

    # Load sparkle emoji
    try:
        sparkle = Image.open(SPARKLE_EMOJI_PATH)
        sparkle_size = 60
        sparkle = sparkle.resize((sparkle_size, sparkle_size), Image.Resampling.LANCZOS)
    except:
        sparkle = None

    # Add text with shadow
    title_text = "decoy daily deals"
    title_font_size = 80
    title_y = current_y + 20

    # Calculate text width for centering
    if font_path:
        temp_font = ImageFont.truetype(font_path, title_font_size)
        bbox = draw.textbbox((0, 0), title_text, font=temp_font)
        text_width = bbox[2] - bbox[0]
    else:
        text_width = len(title_text) * 40  # Estimate

    title_x = (IMAGE_WIDTH - text_width) // 2
    add_text_with_shadow(draw, title_text, (title_x, title_y), title_font_size, font_path, fill='white', shadow_offset=5)

    # Add sparkle emojis on both sides
    if sparkle:
        sparkle_y = title_y + 10
        left_sparkle_x = title_x - sparkle_size - 20
        right_sparkle_x = title_x + text_width + 20

        if sparkle.mode == 'RGBA':
            canvas.paste(sparkle, (left_sparkle_x, sparkle_y), sparkle)
            canvas.paste(sparkle, (right_sparkle_x, sparkle_y), sparkle)
        else:
            canvas.paste(sparkle, (left_sparkle_x, sparkle_y))
            canvas.paste(sparkle, (right_sparkle_x, sparkle_y))

    # Download and process product images
    product_images = []
    print("  Downloading and processing product images...")
    for i, deal in enumerate(deals[:7]):  # Limit to 7 products for better layout
        image_urls = deal.get('image_urls', [])
        brand = deal.get('brand', '')
        if image_urls:
            # Use specific high-quality images for certain brands
            if brand == 'Vuori':
                image_url = 'https://cdn.shopify.com/s/files/1/0022/4008/6074/products/V8003STY_539d9e62-f5d3-4524-ba57-0301aeafb764.jpg?v=1754073098'
            elif brand == 'Mejuri':
                # Use local high-quality image
                try:
                    product_img = Image.open('generated_images/2025-10-27/mejuri_earings.png')
                    product_img = remove_background(product_img)
                    product_images.append(product_img)
                    print(f"    Processed product {i+1}/{min(7, len(deals))}")
                    continue
                except:
                    image_url = image_urls[0]
            else:
                image_url = image_urls[0]

            product_img = download_image(image_url)
            if product_img:
                product_img = remove_background(product_img)
                product_images.append(product_img)
                print(f"    Processed product {i+1}/{min(7, len(deals))}")

    # Define layout positions for products (scattered/collage style)
    # Starting below the title
    content_start_y = title_y + 150
    content_height = IMAGE_HEIGHT - content_start_y - 50

    # Arrange products in a scattered layout
    if len(product_images) >= 1:
        arrange_products_collage(canvas, product_images, content_start_y, content_height)

    # Add decorative icons
    add_decorative_icons(canvas)

    return canvas


def arrange_products_collage(canvas, product_images, start_y, available_height):
    """Arrange products in a clustered collage style with slight overlap"""

    # Define the content area (centered)
    content_width = IMAGE_WIDTH - 200
    content_x_offset = 100

    # Products clustered more tightly in center with slight overlaps
    # Increased sizes for better visibility
    positions = [
        # Format: (x_ratio, y_ratio, size, rotation)
        (0.25, 0.20, 0.38, -18),   # Top left - bigger
        (0.60, 0.18, 0.42, 15),    # Top right - bigger
        (0.30, 0.48, 0.36, -10),   # Middle left - bigger
        (0.68, 0.52, 0.39, 20),    # Middle right - bigger
        (0.48, 0.75, 0.41, -12),   # Bottom center - bigger
    ]

    for i, product_img in enumerate(product_images):
        if i >= len(positions):
            break

        x_ratio, y_ratio, size_ratio, rotation = positions[i]

        # Calculate size
        max_size = int(available_height * size_ratio)

        # Resize product maintaining aspect ratio
        aspect_ratio = product_img.width / product_img.height
        if aspect_ratio > 1:
            # Wider than tall
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            # Taller than wide
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        product_img_resized = product_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Rotate image
        product_img_rotated = product_img_resized.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)

        # Calculate position within content area
        x = content_x_offset + int(content_width * x_ratio)
        y = int(start_y + available_height * y_ratio)

        # Center the image at the position
        x -= product_img_rotated.width // 2
        y -= product_img_rotated.height // 2

        # Paste product
        if product_img_rotated.mode == 'RGBA':
            canvas.paste(product_img_rotated, (x, y), product_img_rotated)
        else:
            canvas.paste(product_img_rotated, (x, y))


def add_decorative_icons(canvas):
    """Add decorative icons (money, gift, credit card, discount sign)"""
    # Larger icons positioned in corners and edges to avoid overlap with products
    icons = [
        # (path, x_position, y_position, size)
        (MONEY_STACK_PATH, 40, 700, 140),      # Left side, lower
        (GIFT_PATH, 50, 1350, 150),            # Bottom left
        (CREDIT_CARD_PATH, 850, 750, 150),     # Right side, lower
        (DISCOUNT_SIGN_PATH, 750, 1680, 120),  # Bottom right - moved from center
    ]

    for icon_path, x, y, size in icons:
        try:
            icon = Image.open(icon_path)
            icon = icon.resize((size, size), Image.Resampling.LANCZOS)

            if icon.mode == 'RGBA':
                canvas.paste(icon, (x, y), icon)
            else:
                canvas.paste(icon, (x, y))
        except Exception as e:
            print(f"  Error adding icon {icon_path}: {e}")


def main():
    """Main function to generate cover page"""
    print("=" * 50)
    print("TikTok Cover Page Generator")
    print("=" * 50)

    # Get font path
    font_path = get_font_path('medium')
    if font_path:
        print(f"Using font: {font_path}")

    # Create output directory
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = os.path.join(OUTPUT_BASE_DIR, today)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Fetch deals
    deals = fetch_deals()
    print(f"Found {len(deals)} deals")

    if not deals:
        print("No deals found. Exiting.")
        return

    # Generate cover page
    try:
        image = create_cover_page(deals, font_path)

        # Save image
        filename = "cover_page.png"
        filepath = os.path.join(output_dir, filename)
        image.save(filepath, 'PNG')
        print(f"\n✓ Cover page saved: {filepath}")
    except Exception as e:
        print(f"✗ Error creating cover page: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 50)


if __name__ == "__main__":
    main()
