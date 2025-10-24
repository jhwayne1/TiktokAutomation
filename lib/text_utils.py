"""
Reusable text rendering utilities
"""

from PIL import ImageFont, ImageDraw
from config import creative_config as config
import os


def get_font(font_type='brand'):
    """
    Get font from configuration

    Args:
        font_type: 'brand', 'discount', or 'title'

    Returns:
        ImageFont or None
    """
    font_config = config.FONTS.get(font_type, config.FONTS['brand'])

    for path in font_config['paths']:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_config['size'])
            except:
                continue

    print(f"Warning: Font {font_type} not found, using default")
    return ImageFont.load_default()


def add_text_with_shadow(draw, text, position, font_type='brand',
                         color_scheme=None, shadow_offset=None):
    """
    Add text with shadow effect

    Args:
        draw: ImageDraw object
        text: Text to render
        position: Tuple (x, y)
        font_type: 'brand', 'discount', or 'title'
        color_scheme: Optional color scheme name
        shadow_offset: Override shadow offset

    Returns:
        Text bounding box
    """
    if color_scheme is None:
        color_scheme = config.ACTIVE_COLOR_SCHEME

    scheme = config.COLOR_SCHEMES[color_scheme]
    font = get_font(font_type)

    if shadow_offset is None:
        shadow_offset = 5

    x, y = position

    # Draw shadow if enabled
    if config.FEATURES['text_shadows']:
        draw.text(
            (x + shadow_offset, y + shadow_offset),
            text,
            font=font,
            fill=scheme['text_shadow']
        )

    # Draw main text
    draw.text((x, y), text, font=font, fill=scheme['text_primary'])

    # Return bounding box
    return draw.textbbox((x, y), text, font=font)


def get_text_dimensions(text, font_type='brand'):
    """
    Get dimensions of text without rendering

    Args:
        text: Text string
        font_type: Font type to use

    Returns:
        Tuple (width, height)
    """
    from PIL import Image
    font = get_font(font_type)

    # Create temporary image to measure text
    temp_img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(temp_img)
    bbox = draw.textbbox((0, 0), text, font=font)

    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    return width, height


def transform_text(text, transform='lowercase'):
    """
    Transform text case

    Args:
        text: Input text
        transform: 'lowercase', 'uppercase', or 'title'

    Returns:
        Transformed text
    """
    if transform == 'lowercase':
        return text.lower()
    elif transform == 'uppercase':
        return text.upper()
    elif transform == 'title':
        return text.title()
    return text


def calculate_centered_position(text, canvas_width, font_type='brand'):
    """
    Calculate x position to center text

    Args:
        text: Text to center
        canvas_width: Width of canvas
        font_type: Font type

    Returns:
        X position
    """
    width, _ = get_text_dimensions(text, font_type)
    return (canvas_width - width) // 2


def add_multiline_text(draw, lines, start_y, canvas_width,
                      font_type='title', line_spacing=None, color_scheme=None):
    """
    Add multiple lines of text, each centered

    Args:
        draw: ImageDraw object
        lines: List of text lines
        start_y: Starting Y position
        canvas_width: Canvas width for centering
        font_type: Font type
        line_spacing: Space between lines
        color_scheme: Color scheme

    Returns:
        Final Y position
    """
    if line_spacing is None:
        line_spacing = config.TEXT_TEMPLATES['end_page'].get('line_spacing', 100)

    current_y = start_y

    for i, line in enumerate(lines):
        x = calculate_centered_position(line, canvas_width, font_type)
        add_text_with_shadow(draw, line, (x, current_y), font_type, color_scheme)

        if i < len(lines) - 1:
            _, height = get_text_dimensions(line, font_type)
            current_y += height + line_spacing

    return current_y
