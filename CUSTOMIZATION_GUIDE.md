# Customization Guide

This project is designed to be modular and easily customizable. You can experiment with different creative strategies without touching the core generation logic.

## Quick Start: Change Your Visual Style

All customization happens in **`config/creative_config.py`**. No need to edit the generation scripts!

## 🎨 Change Color Scheme (30 seconds)

Want a different vibe? Just change one line:

```python
# In config/creative_config.py
ACTIVE_COLOR_SCHEME = 'sunset'  # Try: 'blue_pink', 'sunset', or 'ocean'
```

### Add Your Own Color Scheme

```python
COLOR_SCHEMES = {
    'your_theme': {
        'gradient_start': (255, 100, 150),  # Pink
        'gradient_end': (150, 100, 255),     # Purple
        'text_primary': 'white',
        'text_secondary': '#666666',
        'text_shadow': (180, 180, 180, 200),
        'container_bg': 'white',
    },
}

ACTIVE_COLOR_SCHEME = 'your_theme'
```

## 📐 Change Product Layout (1 minute)

Want products arranged differently?

```python
# In config/creative_config.py
ACTIVE_PRODUCT_POSITION = 'scattered'  # Try: 'clustered', 'scattered', or 'grid'
```

### Create Custom Layout

```python
PRODUCT_POSITIONS = {
    'my_layout': [
        # (x_ratio, y_ratio, size_ratio, rotation_degrees)
        (0.50, 0.30, 0.40, 0),      # Center, large, no rotation
        (0.25, 0.60, 0.30, -15),    # Left, medium, tilted
        (0.75, 0.60, 0.30, 15),     # Right, medium, tilted
        # Add more positions...
    ],
}

ACTIVE_PRODUCT_POSITION = 'my_layout'
```

## 🎯 Reposition Icons (1 minute)

Move decorative icons around:

```python
ACTIVE_ICON_POSITION = 'corners'  # Try: 'default' or 'corners'
```

### Custom Icon Positions

```python
ICON_POSITIONS = {
    'my_icons': [
        # (icon_key, x, y, movement_range)
        ('money', 100, 500, 25),         # Left side, more movement
        ('gift', 900, 500, 20),          # Right side
        ('credit_card', 100, 1500, 15),  # Bottom left
        ('discount_sign', 900, 1500, 15),# Bottom right
    ],
}

ACTIVE_ICON_POSITION = 'my_icons'
```

## 📝 Change Text Content (30 seconds)

Modify what text appears:

```python
TEXT_TEMPLATES = {
    'cover_page': {
        'line1': 'your custom text here',  # Change cover page text
        'shadow_offset': 5,
        'use_sparkles': True,
    },
    'end_page': {
        'line1': 'custom first line',
        'line2': 'custom second line',
        'line_spacing': 100,
    },
    'individual': {
        'discount_format': '{percent}% discount',  # Change format
        'text_transform': 'uppercase',  # Try: 'lowercase', 'uppercase', 'title'
    }
}
```

## 🎬 Animation Settings (1 minute)

Control animation behavior:

```python
ANIMATION = {
    'enabled': True,
    'frames': 60,              # More frames = smoother (but larger file)
    'frame_duration': 50,      # Faster animation (milliseconds per frame)
    'loop': True,
}
```

## 🔧 Font Customization (2 minutes)

Change font sizes:

```python
FONTS = {
    'brand': {
        'weight': 'medium',
        'size': 90,  # Make brand name bigger!
        'paths': [...]
    },
    'discount': {
        'weight': 'light',
        'size': 60,  # Make discount text bigger!
        'paths': [...]
    },
}
```

## 🚀 Feature Flags (Instant)

Turn features on/off:

```python
FEATURES = {
    'background_removal': True,    # Remove product backgrounds
    'text_shadows': True,          # Add shadows to text
    'auto_optimize_images': False, # Optimize file sizes
    'watermark': False,            # Add watermark (coming soon)
}
```

## 🧪 Experimental Features

Try new features:

```python
EXPERIMENTAL = {
    'use_ai_upscaling': False,     # AI upscaling (future)
    'apply_filters': True,         # Image filters
    'filter_type': 'vintage',      # Try: 'vintage', 'vibrant', 'cool', 'warm'
    'add_borders': False,
}
```

## 📦 Advanced: Create Your Own Modules

### Custom Image Processor

Create `lib/custom_processor.py`:

```python
from lib.image_utils import *
from config import creative_config as config

def my_custom_effect(image):
    # Your custom image processing
    return image
```

### Custom Layout Strategy

Create `lib/my_layouts.py`:

```python
from lib.layout_engine import LayoutEngine

class MyCustomLayout(LayoutEngine):
    def custom_positioning(self):
        # Your custom positioning logic
        pass
```

## 🎯 Common Customization Recipes

### Make Everything Bigger
```python
# Increase all font sizes
FONTS['brand']['size'] = 90
FONTS['discount']['size'] = 70
FONTS['title']['size'] = 100

# Increase icon sizes
LAYOUTS['collage']['icon_sizes'] = {
    'money': 180,
    'gift': 200,
    'credit_card': 180,
    'discount_sign': 160,
}
```

### Minimal Style (Less Clutter)
```python
# Use grid layout for clean look
ACTIVE_PRODUCT_POSITION = 'grid'

# Remove icon animations
ANIMATION['enabled'] = False

# Simpler text
TEXT_TEMPLATES['cover_page']['use_sparkles'] = False
```

### Bold & Loud Style
```python
# Use bright colors
COLOR_SCHEMES['bold'] = {
    'gradient_start': (255, 0, 150),
    'gradient_end': (255, 255, 0),
    'text_primary': 'white',
    'text_secondary': '#000000',
    'text_shadow': (0, 0, 0, 255),
    'container_bg': '#FF00FF',
}
ACTIVE_COLOR_SCHEME = 'bold'

# Make text huge
FONTS['title']['size'] = 120
```

## 🔄 Testing Your Changes

After editing `config/creative_config.py`:

```bash
# Test locally
./run.sh

# Or test specific generators
python generate_cover_page.py
python generate_end_page.py
```

Your changes will automatically be used in the next GitHub Actions run!

## 📚 File Structure Reference

```
TiktokAutomation/
├── config/
│   └── creative_config.py     # ← EDIT THIS for most changes
├── lib/
│   ├── image_utils.py         # Reusable image functions
│   ├── text_utils.py          # Reusable text functions
│   ├── api_utils.py           # API and data handling
│   └── layout_engine.py       # Layout calculations
├── generate_*.py              # Generator scripts (rarely edit)
└── CUSTOMIZATION_GUIDE.md     # This file
```

## 💡 Pro Tips

1. **Experiment Fast**: Change `ACTIVE_COLOR_SCHEME` or `ACTIVE_PRODUCT_POSITION` - no code changes needed!

2. **Save Presets**: Create multiple color schemes and layouts, switch between them instantly

3. **A/B Test**: Generate images with different configs, see what performs better on TikTok

4. **Version Control**: Use Git branches to test different creative strategies:
   ```bash
   git checkout -b experiment/new-layout
   # Edit config
   git commit -m "Test new layout"
   ```

5. **Revert Easily**: If you don't like a change, just revert the config file!

## 🆘 Need Help?

- Check `config/creative_config.py` for all available options
- Look at `lib/` modules for reusable components
- Read inline comments in the code
- Test locally before pushing to GitHub

## 🎨 Share Your Themes!

Created an awesome configuration? Share it! Others can copy your theme settings into their `creative_config.py`.

---

**Remember**: The beauty of this modular system is that you can experiment freely without breaking anything. Just edit the config, test, and iterate!
