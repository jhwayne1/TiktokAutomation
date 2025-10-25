#!/usr/bin/env python3
"""
TikTok Image Asset Generator
Automatically pulls data from API and creates promotional images
"""

import os
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from rembg import remove
import math


# Configuration
API_URL = "https://item-api-rosy.vercel.app/api/deals"
LOGO_PATH = "DecoyWizard.png"
OUTPUT_BASE_DIR = "generated_images"
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920

# SF Pro Rounded font paths (fallback to system fonts if not available)
FONT_PATHS_MEDIUM = [
    "/System/Library/Fonts/SFProRounded-Medium.ttf",
    "/System/Library/Fonts/Supplemental/SF-Pro-Rounded-Medium.otf",
    "/Library/Fonts/SF-Pro-Rounded-Medium.otf",
    "/System/Library/Fonts/SF-Pro-Medium.ttf",
]

FONT_PATHS_LIGHT = [
    "/System/Library/Fonts/SFProRounded-Light.ttf",
    "/System/Library/Fonts/Supplemental/SF-Pro-Rounded-Light.otf",
    "/Library/Fonts/SF-Pro-Rounded-Light.otf",
    "/System/Library/Fonts/SF-Pro-Light.ttf",
]

FONT_PATHS_REGULAR = [
    "/System/Library/Fonts/SFProRounded.ttf",
    "/System/Library/Fonts/Supplemental/SF-Pro-Rounded-Regular.otf",
    "/Library/Fonts/SF-Pro-Rounded-Regular.otf",
    "/System/Library/Fonts/SF-Pro.ttf",
]


def get_font_path(weight='regular'):
    """Find available SF Pro Rounded font with specified weight"""
    if weight == 'medium':
        paths = FONT_PATHS_MEDIUM
    elif weight == 'light':
        paths = FONT_PATHS_LIGHT
    else:
        paths = FONT_PATHS_REGULAR

    for path in paths:
        if os.path.exists(path):
            return path

    # If specific weight not found, try regular as fallback
    if weight != 'regular':
        print(f"Warning: SF Pro Rounded {weight} not found, trying regular")
        for path in FONT_PATHS_REGULAR:
            if os.path.exists(path):
                return path

    # If no SF Pro font found, try to use system default
    print("Warning: SF Pro Rounded font not found, using default font")
    return None


def calculate_discount_percentage(current_price, original_price):
    """Calculate discount percentage using the formula: 1-(discount price / full price) * 100"""
    if original_price == 0:
        return 0
    discount = (1 - (current_price / original_price)) * 100
    return round(discount)


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
        print("  Removing background...")
        # Convert to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Remove background
        output = remove(img_byte_arr.read())

        # Convert back to PIL Image
        return Image.open(BytesIO(output))
    except Exception as e:
        print(f"  Error removing background: {e}")
        return image


def create_gradient_background(width, height):
    """Create a gradient background from light blue to pink"""
    # Create a new image
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Define colors (light blue to pink)
    color_start = (190, 227, 248)  # Light blue
    color_end = (239, 198, 237)    # Light pink

    # Create vertical gradient
    for y in range(height):
        # Calculate interpolation factor
        ratio = y / height

        # Interpolate between colors
        r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
        g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
        b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)

        # Draw line
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return img


def add_text_with_font(draw, text, position, font_size, font_path, fill='black', align='left'):
    """Add text to image with specified font"""
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()

        # Get text bbox for alignment
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]

        # Adjust position based on alignment
        x, y = position
        if align == 'center':
            x = x - text_width // 2

        draw.text((x, y), text, font=font, fill=fill)
        return bbox[3] - bbox[1]  # Return text height
    except Exception as e:
        print(f"  Error adding text: {e}")
        # Fallback to default font
        font = ImageFont.load_default()
        draw.text(position, text, font=font, fill=fill)
        return 20


def create_tiktok_image(deal, font_path_medium, font_path_light):
    """Create TikTok image asset for a deal"""
    print(f"Creating image for: {deal.get('brand', 'Unknown')} - {deal.get('name', 'Unknown')}")

    # Create gradient background
    canvas = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT)

    # Load and add logo at the top
    try:
        logo = Image.open(LOGO_PATH)
        # Resize logo to fit (max 300px wide)
        logo_max_width = 300
        logo_ratio = logo_max_width / logo.width
        logo_height = int(logo.height * logo_ratio)
        logo = logo.resize((logo_max_width, logo_height), Image.Resampling.LANCZOS)

        # Center logo at top
        logo_x = (IMAGE_WIDTH - logo_max_width) // 2
        logo_y = 50

        # Paste logo (handle transparency)
        if logo.mode == 'RGBA':
            canvas.paste(logo, (logo_x, logo_y), logo)
        else:
            canvas.paste(logo, (logo_x, logo_y))

        current_y = logo_y + logo_height + 40
    except Exception as e:
        print(f"  Error loading logo: {e}")
        current_y = 100

    # Add brand name and discount in white box
    draw = ImageDraw.Draw(canvas)

    # White box for text
    box_height = 200
    box_y = current_y
    box_margin = 25

    # Draw rounded white rectangle
    box_coords = [box_margin, box_y, IMAGE_WIDTH - box_margin, box_y + box_height]
    draw.rounded_rectangle(box_coords, radius=15, fill='white')

    # Calculate discount percentage first
    current_price = deal.get('current_price', 0)

    # Try to get original price from best_promo_code or estimate from current price
    best_promo = deal.get('best_promo_code', {})
    if best_promo and best_promo.get('price_after_applied'):
        # The current_price might be the original, and price_after_applied is discounted
        # Or vice versa - we need to figure out which is which
        promo_price = best_promo.get('price_after_applied', 0)
        if promo_price < current_price:
            # current_price is original, promo_price is discounted
            original_price = current_price
            discount_price = promo_price
        else:
            # Assume current_price is already discounted
            # Estimate original price
            original_price = current_price * 1.25  # Assume at least 20% off
            discount_price = current_price
    else:
        # Estimate based on typical discount
        discount_price = current_price
        original_price = current_price * 1.25

    discount_percent = calculate_discount_percentage(discount_price, original_price)

    # Calculate text dimensions for centering
    brand_font_size = 70
    discount_font_size = 55
    text_spacing = 15  # Space between brand and discount text

    # Get actual text heights using bounding boxes
    brand = deal.get('brand', '').lower()
    discount_text = f"{discount_percent}% off sitewide"

    # Create temporary fonts to measure text
    if font_path_medium:
        brand_font = ImageFont.truetype(font_path_medium, brand_font_size)
        brand_bbox = draw.textbbox((0, 0), brand, font=brand_font)
        brand_height = brand_bbox[3] - brand_bbox[1]
    else:
        brand_height = brand_font_size

    if font_path_light:
        discount_font = ImageFont.truetype(font_path_light, discount_font_size)
        discount_bbox = draw.textbbox((0, 0), discount_text, font=discount_font)
        discount_height = discount_bbox[3] - discount_bbox[1]
    else:
        discount_height = discount_font_size

    # Total height of text group (using actual measurements)
    total_text_height = brand_height + text_spacing + discount_height

    # Center the text group vertically within the box
    text_group_start_y = box_y + (box_height - total_text_height) // 2

    # Add brand name (lowercase) - SF Pro Rounded Medium
    brand_y = text_group_start_y
    add_text_with_font(draw, brand, (IMAGE_WIDTH // 2, brand_y), brand_font_size, font_path_medium,
                      fill='black', align='center')

    # Add discount text (lowercase) - SF Pro Rounded Light
    discount_y = brand_y + brand_height + text_spacing
    add_text_with_font(draw, discount_text, (IMAGE_WIDTH // 2, discount_y), discount_font_size, font_path_light,
                      fill='#666666', align='center')

    # Download and process product image
    image_urls = deal.get('image_urls', [])
    if image_urls:
        product_img = download_image(image_urls[0])
        if product_img:
            # Remove background
            product_img = remove_background(product_img)

            # Calculate available space for product image
            # Space between bottom of text box and bottom of canvas
            available_space_top = box_y + box_height
            available_space_bottom = IMAGE_HEIGHT
            available_height = available_space_bottom - available_space_top

            # Resize product image to fit nicely (with some padding)
            max_product_width = IMAGE_WIDTH - 100
            max_product_height = available_height - 100  # Leave padding

            # Calculate resize ratio
            width_ratio = max_product_width / product_img.width
            height_ratio = max_product_height / product_img.height
            resize_ratio = min(width_ratio, height_ratio, 1.5)  # Don't upscale too much

            new_width = int(product_img.width * resize_ratio)
            new_height = int(product_img.height * resize_ratio)

            product_img = product_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Center product image vertically between bottom of box and bottom of canvas
            product_x = (IMAGE_WIDTH - new_width) // 2
            product_y = available_space_top + (available_height - new_height) // 2

            # Paste product image
            if product_img.mode == 'RGBA':
                canvas.paste(product_img, (product_x, product_y), product_img)
            else:
                canvas.paste(product_img, (product_x, product_y))

    return canvas


def main():
    """Main function to generate all TikTok images"""
    print("=" * 50)
    print("TikTok Image Asset Generator")
    print("=" * 50)

    # Get font paths for different weights
    font_path_medium = get_font_path('medium')
    font_path_light = get_font_path('light')
    if font_path_medium:
        print(f"Using Medium font: {font_path_medium}")
    if font_path_light:
        print(f"Using Light font: {font_path_light}")

    # Create output directory with today's date
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

    # Generate images for each deal
    for i, deal in enumerate(deals, 1):
        print(f"\n[{i}/{len(deals)}] Processing deal...")
        try:
            # Create image
            image = create_tiktok_image(deal, font_path_medium, font_path_light)

            # Save image
            brand = deal.get('brand', 'unknown').lower().replace(' ', '_')
            short_id = deal.get('short_id', i)
            filename = f"{brand}_{short_id}.png"
            filepath = os.path.join(output_dir, filename)

            image.save(filepath, 'PNG')
            print(f"  ✓ Saved: {filepath}")
        except Exception as e:
            print(f"  ✗ Error processing deal: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 50}")
    print(f"Complete! Generated {len(deals)} images in {output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()
