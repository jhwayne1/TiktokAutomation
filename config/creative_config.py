"""
Creative Configuration
Define your creative strategies here - easily swap between different styles
"""

# Image Dimensions
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920

# API Configuration
API_URL = "https://item-api-rosy.vercel.app/api/deals"

# Asset Paths
ASSETS = {
    'logo': 'DecoyWizard.png',
    'sparkle': 'sparkle-emoji.png',
    'money': 'MoneyStack.png',
    'credit_card': 'CreditCard.png',
    'gift': 'Gift.png',
    'discount_sign': 'discountsign.png',
}

# Font Configuration
FONTS = {
    'brand': {
        'weight': 'medium',
        'size': 70,
        'paths': [
            "/Library/Fonts/SF-Pro-Rounded-Medium.otf",
            "/System/Library/Fonts/SFProRounded-Medium.ttf",
        ]
    },
    'discount': {
        'weight': 'light',
        'size': 55,
        'paths': [
            "/Library/Fonts/SF-Pro-Rounded-Light.otf",
            "/System/Library/Fonts/SFProRounded-Light.ttf",
        ]
    },
    'title': {
        'weight': 'medium',
        'size': 80,
        'paths': [
            "/Library/Fonts/SF-Pro-Rounded-Medium.otf",
            "/System/Library/Fonts/SFProRounded-Medium.ttf",
        ]
    }
}

# Color Schemes - Easy to swap!
COLOR_SCHEMES = {
    'blue_pink': {
        'gradient_start': (190, 227, 248),  # Light blue
        'gradient_end': (239, 198, 237),    # Light pink
        'text_primary': 'white',
        'text_secondary': '#666666',
        'text_shadow': (180, 180, 180, 200),
        'container_bg': 'white',
    },
    'sunset': {
        'gradient_start': (255, 183, 178),  # Coral
        'gradient_end': (255, 218, 185),    # Peach
        'text_primary': 'white',
        'text_secondary': '#555555',
        'text_shadow': (150, 150, 150, 200),
        'container_bg': 'white',
    },
    'ocean': {
        'gradient_start': (130, 204, 221),  # Sky blue
        'gradient_end': (140, 233, 253),    # Aqua
        'text_primary': 'white',
        'text_secondary': '#444444',
        'text_shadow': (100, 100, 100, 200),
        'container_bg': 'white',
    },
}

# Active color scheme - change this to experiment!
ACTIVE_COLOR_SCHEME = 'blue_pink'

# Layout Configurations
LAYOUTS = {
    'individual_product': {
        'logo_max_width': 350,
        'logo_y': 60,
        'text_box_height': 200,
        'text_box_margin': 25,
        'text_box_radius': 15,
        'brand_discount_spacing': 15,
        'content_padding': 100,
    },
    'collage': {
        'logo_max_width': 350,
        'logo_y': 60,
        'title_y_offset': 40,
        'sparkle_size': 60,
        'sparkle_padding': 20,
        'content_start_offset': 150,
        'content_margin': 200,  # Margins on left/right
        'icon_sizes': {
            'money': 140,
            'gift': 150,
            'credit_card': 150,
            'discount_sign': 120,
        },
    }
}

# Product Positioning Templates
PRODUCT_POSITIONS = {
    'clustered': [
        # (x_ratio, y_ratio, size_ratio, rotation)
        (0.25, 0.20, 0.38, -18),
        (0.60, 0.18, 0.42, 15),
        (0.30, 0.48, 0.36, -10),
        (0.68, 0.52, 0.39, 20),
        (0.48, 0.75, 0.41, -12),
    ],
    'scattered': [
        (0.15, 0.25, 0.35, -20),
        (0.70, 0.15, 0.40, 15),
        (0.25, 0.55, 0.30, -10),
        (0.75, 0.50, 0.35, 20),
        (0.45, 0.80, 0.32, -15),
    ],
    'grid': [
        (0.30, 0.25, 0.35, 0),
        (0.70, 0.25, 0.35, 0),
        (0.30, 0.55, 0.35, 0),
        (0.70, 0.55, 0.35, 0),
        (0.50, 0.80, 0.35, 0),
    ],
}

# Active product positioning style
ACTIVE_PRODUCT_POSITION = 'clustered'

# Icon Positions
ICON_POSITIONS = {
    'default': [
        # (x, y, movement_range_for_animation)
        ('money', 40, 700, 20),
        ('gift', 50, 1350, 15),
        ('credit_card', 850, 750, 18),
        ('discount_sign', 750, 1680, 12),
    ],
    'corners': [
        ('money', 50, 600, 20),
        ('gift', 50, 1650, 15),
        ('credit_card', 850, 600, 18),
        ('discount_sign', 850, 1650, 12),
    ],
}

# Active icon positioning
ACTIVE_ICON_POSITION = 'default'

# Text Templates
TEXT_TEMPLATES = {
    'cover_page': {
        'line1': 'decoy daily deals',
        'shadow_offset': 5,
        'use_sparkles': True,
    },
    'end_page': {
        'line1': 'grab discounts',
        'line2': 'link in bio',
        'line_spacing': 100,
        'shadow_offset': 5,
        'use_sparkles': True,
    },
    'individual': {
        'discount_format': '{percent}% off sitewide',
        'text_transform': 'lowercase',  # 'lowercase', 'uppercase', or 'title'
    }
}

# Animation Settings
ANIMATION = {
    'enabled': True,
    'frames': 30,
    'frame_duration': 100,  # milliseconds
    'loop': True,
}

# Output Settings
OUTPUT = {
    'base_dir': 'generated_images',
    'date_format': '%Y-%m-%d',
    'include_timestamp': False,
    'formats': {
        'individual': 'png',
        'cover': 'png',
        'cover_animated': 'gif',
        'end': 'png',
    }
}

# Feature Flags - Turn features on/off easily
FEATURES = {
    'background_removal': True,
    'text_shadows': True,
    'auto_optimize_images': False,
    'generate_thumbnails': False,
    'watermark': False,
}

# Experimental Features
EXPERIMENTAL = {
    'use_ai_upscaling': False,
    'apply_filters': False,
    'filter_type': None,  # 'vintage', 'vibrant', 'cool', 'warm'
    'add_borders': False,
    'border_width': 0,
}
