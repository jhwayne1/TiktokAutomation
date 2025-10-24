# TikTok Image Asset Generator 🎨

Automated system that generates professional TikTok promotional images daily from deal data sourced from an API.

![Automated Generation](https://img.shields.io/badge/Automated-Daily%20at%207AM-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Status](https://img.shields.io/badge/Status-Production-success)

## Features

- Fetches deals from API endpoint
- Creates individual branded promotional images (1080 x 1920)
- Generates a collage-style cover page with all daily deals
- Automatic background removal from product images
- Beautiful gradient backgrounds (light blue to pink)
- Uses SF Pro Rounded font for professional appearance
- Calculates discount percentages automatically
- Organizes images by date
- All text in lowercase for consistent branding
- Text with shadow effects on cover page

## Requirements

- Python 3.7+
- Virtual environment (venv)

## Installation

1. Clone or download this repository

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Simply run the master script to generate all daily assets:

```bash
# Easy way - use the convenience script
./run.sh

# Or manually
source venv/bin/activate
python generate_all_images.py
```

The script will:
1. Fetch the latest deals from the API
2. Download product images
3. Remove backgrounds from images
4. Generate individual branded promotional images
5. Generate a collage-style cover page with all products
6. Save all images to `generated_images/YYYY-MM-DD/` folder

### Individual Scripts

You can also run the generators separately:

```bash
# Generate only individual product images
python generate_tiktok_images.py

# Generate only the cover page
python generate_cover_page.py
```

## Output

Images are saved in the following structure:
```
generated_images/
  2025-10-24/
    cover_page.png                # Static collage cover page
    cover_page_animated.gif       # Animated cover with floating icons
    end_page.png                  # End page with CTA
    vuori_g71bnm.png             # Individual product images
    monos_e9hdu5.png
    legator_34grjy.png
    elegoo_l4n2od.png
    popov_leather®_jntdv3.png
```

### Individual Product Images (5-7 images)
Each image includes:
- DecoyWizard logo at the top
- White text container with:
  - Brand name (SF Pro Rounded Medium, lowercase)
  - Discount percentage + "off sitewide" (SF Pro Rounded Light)
- Product image with background removed (centered)
- Gradient background (blue to pink)

### Cover Page (cover_page.png)
Static version includes:
- DecoyWizard logo at the top
- "decoy daily deals" text with sparkle emojis and shadow effect
- All product images arranged in a clustered collage layout
- Decorative icons (money stack, gift, credit card, discount sign)
- Gradient background (blue to pink)

### Animated Cover Page (cover_page_animated.gif)
Same as cover page but with:
- Smooth floating animation on all icons
- 30 frames, 3-second loop
- Each icon moves independently with sine wave motion
- Perfect for grabbing attention on TikTok

### End Page (end_page.png)
Call-to-action page with:
- "grab discounts" and "link in bio" on two lines
- Same layout as cover page (identical product and icon positioning)
- White text with shadow effect

## Configuration

You can modify the following settings in `generate_tiktok_images.py`:

- `API_URL`: The API endpoint to fetch deals from
- `IMAGE_WIDTH`: Output image width (default: 1080)
- `IMAGE_HEIGHT`: Output image height (default: 1920)
- `LOGO_PATH`: Path to your logo file

## Discount Calculation

The script uses this formula to calculate discounts:
```
discount_percentage = (1 - (discount_price / full_price)) * 100
```

## Font

The script uses SF Pro Rounded font. If not available on your system, it falls back to default fonts.

## Dependencies

- **requests**: API calls and image downloads
- **Pillow (PIL)**: Image manipulation
- **rembg**: Background removal from images
- **onnxruntime**: Required by rembg for ML-based background removal

## Troubleshooting

### Missing onnxruntime
If you get an error about `onnxruntime`, install it manually:
```bash
pip install onnxruntime
```

### Font not found
The script will automatically fall back to system fonts if SF Pro Rounded is not available.

### API errors
Ensure you have internet connectivity and the API endpoint is accessible.

## Automated Daily Generation with GitHub Actions

This project includes a GitHub Actions workflow that automatically generates images every day at 7:00 AM EST.

### Quick Setup

1. **Create a GitHub repository** and push this code
2. **The workflow will automatically run** at 7 AM EST daily
3. **Download images** from the Actions artifacts or view them in the repo

For detailed setup instructions, see [GITHUB_SETUP.md](GITHUB_SETUP.md)

### What Gets Automated

- ✅ All individual product images
- ✅ Cover page (static)
- ✅ End page
- ✅ Images are saved as artifacts (available for 30 days)
- ✅ Optional: Auto-commit to repository

### Manual Trigger

You can also manually trigger the workflow:
1. Go to your repository's "Actions" tab
2. Select "Generate Daily TikTok Images"
3. Click "Run workflow"

## Project Structure

```
TiktokAutomation/
├── .github/
│   └── workflows/
│       └── generate-daily-images.yml  # GitHub Actions workflow
├── generated_images/                  # Output directory
├── generate_all_images.py            # Master script
├── generate_tiktok_images.py         # Individual products
├── generate_cover_page.py            # Static cover
├── generate_animated_cover.py        # Animated GIF cover
├── generate_end_page.py              # End page/CTA
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── GITHUB_SETUP.md                   # Setup guide
```

## License

This project is for personal use.
