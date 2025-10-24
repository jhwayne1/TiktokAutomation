#!/usr/bin/env python3
"""
Master TikTok Image Generator
Generates individual product images, cover page, and end page
"""

import os
import sys
from datetime import datetime

# Import the individual generators
import generate_tiktok_images
import generate_cover_page
import generate_end_page


def main():
    """Generate all TikTok assets for today"""
    print("=" * 60)
    print("TikTok Daily Image Generator")
    print("Generating all assets for today's deals")
    print("=" * 60)
    print()

    # Generate individual product images
    print("STEP 1: Generating individual product images...")
    print("-" * 60)
    try:
        generate_tiktok_images.main()
    except Exception as e:
        print(f"Error generating product images: {e}")
        import traceback
        traceback.print_exc()

    print()
    print()

    # Generate cover page
    print("STEP 2: Generating cover page...")
    print("-" * 60)
    try:
        generate_cover_page.main()
    except Exception as e:
        print(f"Error generating cover page: {e}")
        import traceback
        traceback.print_exc()

    print()
    print()

    # Generate end page
    print("STEP 3: Generating end page...")
    print("-" * 60)
    try:
        generate_end_page.main()
    except Exception as e:
        print(f"Error generating end page: {e}")
        import traceback
        traceback.print_exc()

    print()
    print("=" * 60)
    print("All images generated successfully!")

    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = os.path.join("generated_images", today)
    print(f"Check your images at: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
