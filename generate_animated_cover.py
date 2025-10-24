#!/usr/bin/env python3
"""
TikTok Animated Cover Page Generator
Creates an animated GIF cover page with floating icons
"""

import os
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from rembg import remove
import math


# Configuration
API_URL = "https://item-api-rosy.vercel.app/api/deals"
LOGO_PATH = "DecoyWizard.png"
OUTPUT_BASE_DIR = "generated_images"
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920
NUM_FRAMES = 30  # Number of frames in the animation
FRAME_DURATION = 100  # Duration of each frame in milliseconds

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


def add_text_with_shadow(draw, text, position, font_size, font_path, fill='white', shadow_offset=5):
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


def calculate_floating_position(base_x, base_y, frame, total_frames, movement_range=15):
    """Calculate floating position for an icon using a smooth sine wave"""
    # Use sine wave for smooth up/down motion
    progress = (frame / total_frames) * 2 * math.pi
    offset_y = math.sin(progress) * movement_range

    # Slight horizontal sway
    offset_x = math.sin(progress * 0.7) * (movement_range * 0.5)

    return int(base_x + offset_x), int(base_y + offset_y)


def create_frame(frame_num, total_frames, base_canvas, logo, sparkle, product_images,
                 font_path, title_x, title_y, text_width, content_start_y, content_height,
                 icon_data):
    """Create a single frame of the animation"""
    # Create a copy of the base canvas
    canvas = base_canvas.copy()

    # Paste logo (static)
    logo_x = (IMAGE_WIDTH - logo.width) // 2
    logo_y = 60
    if logo.mode == 'RGBA':
        canvas.paste(logo, (logo_x, logo_y), logo)
    else:
        canvas.paste(logo, (logo_x, logo_y))

    # Add text with shadow
    draw = ImageDraw.Draw(canvas, 'RGBA')
    title_text = "decoy daily deals"
    title_font_size = 80
    add_text_with_shadow(draw, title_text, (title_x, title_y), title_font_size, font_path, fill='white', shadow_offset=5)

    # Add sparkles (static)
    if sparkle:
        sparkle_y = title_y + 10
        left_sparkle_x = title_x - sparkle.width - 20
        right_sparkle_x = title_x + text_width + 20

        if sparkle.mode == 'RGBA':
            canvas.paste(sparkle, (left_sparkle_x, sparkle_y), sparkle)
            canvas.paste(sparkle, (right_sparkle_x, sparkle_y), sparkle)
        else:
            canvas.paste(sparkle, (left_sparkle_x, sparkle_y))
            canvas.paste(sparkle, (right_sparkle_x, sparkle_y))

    # Arrange products (static)
    arrange_products_collage(canvas, product_images, content_start_y, content_height)

    # Add decorative icons with floating animation
    add_animated_icons(canvas, frame_num, total_frames, icon_data)

    return canvas


def arrange_products_collage(canvas, product_images, start_y, available_height):
    """Arrange products in a clustered collage style with slight overlap"""
    content_width = IMAGE_WIDTH - 200
    content_x_offset = 100

    positions = [
        (0.25, 0.20, 0.38, -18),
        (0.60, 0.18, 0.42, 15),
        (0.30, 0.48, 0.36, -10),
        (0.68, 0.52, 0.39, 20),
        (0.48, 0.75, 0.41, -12),
    ]

    for i, product_img in enumerate(product_images):
        if i >= len(positions):
            break

        x_ratio, y_ratio, size_ratio, rotation = positions[i]
        max_size = int(available_height * size_ratio)

        aspect_ratio = product_img.width / product_img.height
        if aspect_ratio > 1:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        product_img_resized = product_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        product_img_rotated = product_img_resized.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)

        x = content_x_offset + int(content_width * x_ratio)
        y = int(start_y + available_height * y_ratio)

        x -= product_img_rotated.width // 2
        y -= product_img_rotated.height // 2

        if product_img_rotated.mode == 'RGBA':
            canvas.paste(product_img_rotated, (x, y), product_img_rotated)
        else:
            canvas.paste(product_img_rotated, (x, y))


def add_animated_icons(canvas, frame_num, total_frames, icon_data):
    """Add decorative icons with floating animation"""
    for icon, base_x, base_y, movement_range in icon_data:
        # Calculate floating position
        x, y = calculate_floating_position(base_x, base_y, frame_num, total_frames, movement_range)

        if icon.mode == 'RGBA':
            canvas.paste(icon, (x, y), icon)
        else:
            canvas.paste(icon, (x, y))


def create_animated_cover(deals, font_path):
    """Create animated TikTok cover page with floating icons"""
    print("Creating animated cover page...")

    # Create base gradient background
    base_canvas = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT)

    # Load logo
    try:
        logo = Image.open(LOGO_PATH)
        logo_max_width = 350
        logo_ratio = logo_max_width / logo.width
        logo_height = int(logo.height * logo_ratio)
        logo = logo.resize((logo_max_width, logo_height), Image.Resampling.LANCZOS)
        current_y = 60 + logo_height + 40
    except Exception as e:
        print(f"  Error loading logo: {e}")
        logo = None
        current_y = 100

    # Load sparkle emoji
    try:
        sparkle = Image.open(SPARKLE_EMOJI_PATH)
        sparkle_size = 60
        sparkle = sparkle.resize((sparkle_size, sparkle_size), Image.Resampling.LANCZOS)
    except:
        sparkle = None

    # Calculate text position
    title_text = "decoy daily deals"
    title_font_size = 80
    title_y = current_y + 20

    if font_path:
        temp_font = ImageFont.truetype(font_path, title_font_size)
        temp_draw = ImageDraw.Draw(base_canvas)
        bbox = temp_draw.textbbox((0, 0), title_text, font=temp_font)
        text_width = bbox[2] - bbox[0]
    else:
        text_width = len(title_text) * 40

    title_x = (IMAGE_WIDTH - text_width) // 2

    # Download and process product images
    product_images = []
    print("  Downloading and processing product images...")
    for i, deal in enumerate(deals[:5]):
        image_urls = deal.get('image_urls', [])
        if image_urls:
            product_img = download_image(image_urls[0])
            if product_img:
                product_img = remove_background(product_img)
                product_images.append(product_img)
                print(f"    Processed product {i+1}/{min(5, len(deals))}")

    content_start_y = title_y + 150
    content_height = IMAGE_HEIGHT - content_start_y - 50

    # Load and prepare icons
    print("  Loading decorative icons...")
    icon_data = []
    icon_configs = [
        (MONEY_STACK_PATH, 40, 700, 140, 20),      # path, x, y, size, movement_range
        (GIFT_PATH, 50, 1350, 150, 15),
        (CREDIT_CARD_PATH, 850, 750, 150, 18),
        (DISCOUNT_SIGN_PATH, 750, 1680, 120, 12),
    ]

    for icon_path, x, y, size, movement in icon_configs:
        try:
            icon = Image.open(icon_path)
            icon = icon.resize((size, size), Image.Resampling.LANCZOS)
            icon_data.append((icon, x, y, movement))
        except Exception as e:
            print(f"  Error loading icon {icon_path}: {e}")

    # Generate frames
    print(f"  Generating {NUM_FRAMES} frames...")
    frames = []
    for i in range(NUM_FRAMES):
        frame = create_frame(i, NUM_FRAMES, base_canvas, logo, sparkle, product_images,
                           font_path, title_x, title_y, text_width, content_start_y,
                           content_height, icon_data)
        frames.append(frame)
        if (i + 1) % 10 == 0:
            print(f"    Generated frame {i+1}/{NUM_FRAMES}")

    return frames


def main():
    """Main function to generate animated cover page"""
    print("=" * 50)
    print("TikTok Animated Cover Page Generator")
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

    # Generate animated cover page
    try:
        frames = create_animated_cover(deals, font_path)

        # Save as GIF
        filename = "cover_page_animated.gif"
        filepath = os.path.join(output_dir, filename)

        print(f"\n  Saving animated GIF...")
        frames[0].save(
            filepath,
            save_all=True,
            append_images=frames[1:],
            duration=FRAME_DURATION,
            loop=0,  # Loop forever
            optimize=False
        )

        print(f"✓ Animated cover page saved: {filepath}")

        file_size = os.path.getsize(filepath) / (1024 * 1024)  # Size in MB
        print(f"  File size: {file_size:.2f} MB")

    except Exception as e:
        print(f"✗ Error creating animated cover page: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 50)


if __name__ == "__main__":
    main()
