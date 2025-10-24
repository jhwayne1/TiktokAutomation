"""
Reusable image manipulation utilities
"""

from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
from rembg import remove as remove_bg
import requests
from config import creative_config as config


def create_gradient_background(width, height, color_scheme=None):
    """
    Create a gradient background

    Args:
        width: Image width
        height: Image height
        color_scheme: Optional color scheme name, uses active scheme if None

    Returns:
        PIL Image with gradient
    """
    if color_scheme is None:
        color_scheme = config.ACTIVE_COLOR_SCHEME

    scheme = config.COLOR_SCHEMES[color_scheme]
    img = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    color_start = scheme['gradient_start']
    color_end = scheme['gradient_end']

    for y in range(height):
        ratio = y / height
        r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
        g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
        b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return img


def download_image(url, timeout=10):
    """
    Download image from URL

    Args:
        url: Image URL
        timeout: Request timeout in seconds

    Returns:
        PIL Image or None if failed
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None


def remove_background(image):
    """
    Remove background from image

    Args:
        image: PIL Image

    Returns:
        PIL Image with background removed
    """
    if not config.FEATURES['background_removal']:
        return image

    try:
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        output = remove_bg(img_byte_arr.read())
        return Image.open(BytesIO(output))
    except Exception as e:
        print(f"Error removing background: {e}")
        return image


def load_and_resize_asset(asset_key, size=None):
    """
    Load asset from config and optionally resize

    Args:
        asset_key: Key in ASSETS dict
        size: Tuple (width, height) or single int for square

    Returns:
        PIL Image or None
    """
    try:
        asset_path = config.ASSETS[asset_key]
        img = Image.open(asset_path)

        if size:
            if isinstance(size, int):
                size = (size, size)
            img = img.resize(size, Image.Resampling.LANCZOS)

        return img
    except Exception as e:
        print(f"Error loading asset {asset_key}: {e}")
        return None


def resize_maintaining_aspect(image, max_width=None, max_height=None):
    """
    Resize image maintaining aspect ratio

    Args:
        image: PIL Image
        max_width: Maximum width
        max_height: Maximum height

    Returns:
        Resized PIL Image
    """
    aspect_ratio = image.width / image.height

    if max_width and max_height:
        width_ratio = max_width / image.width
        height_ratio = max_height / image.height
        ratio = min(width_ratio, height_ratio)
    elif max_width:
        ratio = max_width / image.width
    elif max_height:
        ratio = max_height / image.height
    else:
        return image

    new_width = int(image.width * ratio)
    new_height = int(image.height * ratio)

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def paste_with_transparency(canvas, image, position):
    """
    Paste image onto canvas handling transparency

    Args:
        canvas: PIL Image (background)
        image: PIL Image to paste
        position: Tuple (x, y)
    """
    if image.mode == 'RGBA':
        canvas.paste(image, position, image)
    else:
        canvas.paste(image, position)


def apply_filter(image, filter_type):
    """
    Apply experimental filter to image

    Args:
        image: PIL Image
        filter_type: 'vintage', 'vibrant', 'cool', 'warm'

    Returns:
        Filtered PIL Image
    """
    if not config.EXPERIMENTAL['apply_filters']:
        return image

    # Placeholder for filter logic
    filters = {
        'vintage': ImageFilter.SHARPEN,
        'vibrant': ImageFilter.EDGE_ENHANCE,
        'cool': ImageFilter.BLUR,
        'warm': ImageFilter.SMOOTH,
    }

    if filter_type in filters:
        return image.filter(filters[filter_type])

    return image


def optimize_image(image):
    """
    Optimize image size and quality

    Args:
        image: PIL Image

    Returns:
        Optimized PIL Image
    """
    if not config.FEATURES['auto_optimize_images']:
        return image

    # Placeholder for optimization logic
    return image
