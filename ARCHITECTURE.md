# Architecture Overview

This project follows a modular, configuration-driven architecture that separates concerns and enables rapid experimentation.

## Design Principles

1. **Configuration Over Code**: Change visual styles by editing config, not code
2. **Reusable Components**: DRY principle - write once, use everywhere
3. **Easy Experimentation**: Swap layouts, colors, and styles instantly
4. **No Breaking Changes**: Add new features without touching existing code

## Directory Structure

```
TiktokAutomation/
├── config/                         # Configuration Layer
│   └── creative_config.py         # All customization happens here
│
├── lib/                           # Reusable Components
│   ├── image_utils.py            # Image manipulation functions
│   ├── text_utils.py             # Text rendering functions
│   ├── api_utils.py              # API and data handling
│   └── layout_engine.py          # Positioning and layout logic
│
├── templates/                     # Custom Templates (optional)
│   └── simple_template.py        # Example custom generator
│
├── generate_*.py                  # Generator Scripts
│   ├── generate_all_images.py   # Master orchestrator
│   ├── generate_tiktok_images.py# Individual products
│   ├── generate_cover_page.py   # Static cover
│   ├── generate_animated_cover.py# Animated cover
│   └── generate_end_page.py     # End/CTA page
│
└── .github/workflows/             # Automation
    └── generate-daily-images.yml # GitHub Actions workflow
```

## Layer Architecture

### 1. Configuration Layer (`config/`)

**Purpose**: Single source of truth for all visual and behavioral settings

**What Lives Here**:
- Color schemes
- Font configurations
- Layout templates
- Product positioning strategies
- Icon configurations
- Text templates
- Feature flags
- Experimental settings

**Why**:
- Change visual style without touching code
- A/B test different strategies easily
- Version control your creative decisions
- Share configurations between team members

### 2. Component Layer (`lib/`)

**Purpose**: Reusable, tested functions that do one thing well

**Modules**:

#### `image_utils.py`
- Gradient backgrounds
- Image downloading
- Background removal
- Asset loading and resizing
- Image filters (experimental)

#### `text_utils.py`
- Font loading from config
- Text with shadow effects
- Text measurement and positioning
- Multi-line text rendering
- Text transformations (case, etc.)

#### `api_utils.py`
- Fetch deals from API
- Calculate discounts
- Extract and format deal information
- Data transformation utilities

#### `layout_engine.py`
- Position calculations
- Centering algorithms
- Floating animation math
- Layout strategy patterns

**Why**:
- Write once, use everywhere
- Easy to test in isolation
- Add new features without breaking existing code
- Clear separation of concerns

### 3. Generator Layer (Root `generate_*.py` files)

**Purpose**: Orchestrate components to create specific output types

**Pattern**:
```python
# Import components
from lib.image_utils import create_gradient_background
from lib.text_utils import add_text_with_shadow
from lib.api_utils import fetch_deals
from config import creative_config as config

def generate_something():
    # 1. Fetch data
    deals = fetch_deals()

    # 2. Create canvas
    canvas = create_gradient_background(config.IMAGE_WIDTH, config.IMAGE_HEIGHT)

    # 3. Use components to build image
    # ...

    # 4. Save
    canvas.save(output_path)
```

**Why**:
- Each generator focuses on one output type
- Easy to add new generator types
- Minimal code duplication
- Clear, readable flow

### 4. Template Layer (`templates/`)

**Purpose**: Examples and custom generators built on top of components

**Use Cases**:
- Experimental new designs
- One-off special content
- Learning how to use the system
- Sharing reusable patterns

## Data Flow

```
┌─────────────────┐
│   GitHub Actions│  Scheduled trigger (7 AM)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ generate_all.py │  Master orchestrator
└────────┬────────┘
         │
         ├──────────────────────┬──────────────────────┬─────────────────┐
         ▼                      ▼                      ▼                 ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│generate_tiktok   │  │generate_cover    │  │generate_animated │  │generate_end      │
│_images.py        │  │_page.py          │  │_cover.py         │  │_page.py          │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                      │                     │
         │     ┌───────────────┴──────────────────────┴─────────────────────┘
         │     │
         ▼     ▼
    ┌─────────────────────────────┐
    │    lib/* Components         │  Reusable functions
    │  - image_utils              │
    │  - text_utils               │
    │  - api_utils                │
    │  - layout_engine            │
    └──────────┬──────────────────┘
               │
               ▼
    ┌─────────────────────────────┐
    │  config/creative_config.py  │  Configuration
    │  - Colors, fonts, layouts   │
    │  - Feature flags            │
    └─────────────────────────────┘
               │
               ▼
    ┌─────────────────────────────┐
    │    Generated Images         │  Output
    │  generated_images/YYYY-MM-DD│
    └─────────────────────────────┘
```

## Configuration-Driven Design

### Example: Changing Color Scheme

**Without Modular Design** (bad):
```python
# Edit in 5 different files
draw.line([(0, y), (width, y)], fill=(190, 227, 248))  # File 1
draw.line([(0, y), (width, y)], fill=(190, 227, 248))  # File 2
# ... etc
```

**With Modular Design** (good):
```python
# Edit once in config
ACTIVE_COLOR_SCHEME = 'sunset'  # Done!
```

### Example: Adding New Generator

**Steps**:
1. Create new file: `generate_story.py`
2. Import components from `lib/`
3. Use config from `config/creative_config.py`
4. Generate and save

**No need to**:
- Rewrite image processing
- Rewrite text rendering
- Copy-paste layout code
- Change existing generators

## Extension Points

### Add New Color Scheme
```python
# config/creative_config.py
COLOR_SCHEMES['neon'] = {
    'gradient_start': (255, 0, 255),
    'gradient_end': (0, 255, 255),
    # ...
}
```

### Add New Layout Strategy
```python
# config/creative_config.py
PRODUCT_POSITIONS['circle'] = [
    # Define positions in a circle pattern
]
```

### Add New Component
```python
# lib/my_component.py
def my_new_feature(image, config):
    # Your logic
    return processed_image
```

### Add New Generator
```python
# generate_my_content.py
from lib import *
from config import creative_config as config

def main():
    # Use components to create new content type
    pass
```

## Testing Strategy

### Unit Tests (Future)
```python
# tests/test_image_utils.py
def test_gradient_background():
    img = create_gradient_background(100, 100, 'blue_pink')
    assert img.size == (100, 100)
```

### Integration Tests
```bash
# Test individual generators
python generate_cover_page.py

# Test full workflow
python generate_all_images.py
```

### Visual Regression (Future)
- Save reference images
- Compare generated vs. expected
- Flag visual differences

## Performance Considerations

### Current Optimizations
- Pillow for fast image processing
- Async API calls (could be added)
- Reuse loaded assets within session
- Efficient gradient generation

### Future Optimizations
- Parallel image generation
- Caching downloaded images
- Progressive rendering
- GPU acceleration for filters

## Backwards Compatibility

### Version Policy
- Config changes: Non-breaking (add new, keep old)
- Component changes: Maintain function signatures
- Generator changes: Independent, can evolve freely

### Migration Path
If breaking changes needed:
1. Create new config key
2. Support both old and new
3. Deprecation warning
4. Remove old after transition period

## Best Practices

### For Developers

1. **Add to Config First**: New features should be configurable
2. **Write Reusable Components**: If you copy-paste, refactor
3. **Document Configuration**: Add comments in config file
4. **Test Locally**: Run generators before pushing
5. **Keep Generators Thin**: Logic goes in `lib/`, orchestration in generators

### For Designers

1. **Experiment in Config**: Try different colors, layouts, sizes
2. **Save Presets**: Create named configurations for different styles
3. **Branch for Experiments**: Use Git branches to test ideas
4. **Share Configs**: Export your theme settings for others

### For Content Creators

1. **Use Feature Flags**: Turn features on/off without code
2. **A/B Test Configs**: Generate with different settings
3. **Track What Works**: Note which configs perform best
4. **Request Features**: Tell developers what you need

## Future Enhancements

### Planned
- [ ] More layout templates
- [ ] Advanced animation options
- [ ] Image filters and effects
- [ ] Template gallery/marketplace
- [ ] Visual config editor (GUI)
- [ ] Analytics integration

### Ideas
- [ ] AI-generated text
- [ ] Dynamic font sizing based on text length
- [ ] Smart product clustering
- [ ] Brand-specific themes
- [ ] Multi-language support

---

**Key Takeaway**: This architecture makes it easy to experiment and extend without breaking existing functionality. Config-driven design + reusable components = rapid iteration! 🚀
