"""
Example Template: Simple Image Generator
Demonstrates how to use the modular components to create custom generators
"""

import os
from datetime import datetime
from PIL import ImageDraw

# Import reusable components
from lib.image_utils import create_gradient_background, load_and_resize_asset, paste_with_transparency
from lib.text_utils import add_text_with_shadow, calculate_centered_position
from lib.api_utils import fetch_deals, extract_deal_info
from lib.layout_engine import LayoutEngine
from config import creative_config as config


def generate_simple_image(deal_info, output_path):
    """
    Generate a simple product image using modular components

    This is an example of how easy it is to create new generators
    using the reusable components.
    """

    # 1. Create background using config
    canvas = create_gradient_background(config.IMAGE_WIDTH, config.IMAGE_HEIGHT)

    # 2. Set up layout engine
    layout = LayoutEngine(config.IMAGE_WIDTH, config.IMAGE_HEIGHT)

    # 3. Add logo
    logo = load_and_resize_asset('logo', size=(300, 100))
    if logo:
        logo_x, logo_y = layout.get_logo_position(logo.width, logo.height)
        paste_with_transparency(canvas, logo, (logo_x, logo_y))

    # 4. Add text
    draw = ImageDraw.Draw(canvas, 'RGBA')

    brand_text = deal_info['brand']
    brand_x = calculate_centered_position(brand_text, config.IMAGE_WIDTH, 'brand')
    brand_y = 400

    add_text_with_shadow(draw, brand_text, (brand_x, brand_y), 'brand')

    # 5. Save
    canvas.save(output_path, 'PNG')
    print(f"✓ Saved: {output_path}")


def main():
    """Example main function"""
    print("Simple Template Generator Example")
    print("=" * 50)

    # Fetch deals
    deals = fetch_deals(max_deals=1)

    if not deals:
        print("No deals found")
        return

    # Process first deal
    deal_info = extract_deal_info(deals[0])

    # Generate output path
    today = datetime.now().strftime(config.OUTPUT['date_format'])
    output_dir = os.path.join(config.OUTPUT['base_dir'], today, 'templates')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"simple_{deal_info['short_id']}.png")

    # Generate image
    generate_simple_image(deal_info, output_path)

    print("=" * 50)
    print("Done! Check the templates folder.")


if __name__ == "__main__":
    main()
