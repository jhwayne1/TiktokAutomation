"""
Layout engine for positioning elements
"""

from config import creative_config as config
import math


class LayoutEngine:
    """
    Handles positioning and layout calculations
    """

    def __init__(self, canvas_width, canvas_height):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def get_logo_position(self, logo_width, logo_height, layout_type='individual_product'):
        """Get centered logo position"""
        layout = config.LAYOUTS[layout_type]
        x = (self.canvas_width - logo_width) // 2
        y = layout['logo_y']
        return x, y

    def get_text_box_dimensions(self, layout_type='individual_product'):
        """Get text container dimensions"""
        layout = config.LAYOUTS[layout_type]
        margin = layout['text_box_margin']

        width = self.canvas_width - (2 * margin)
        height = layout['text_box_height']
        x = margin
        y = None  # Will be calculated based on logo position

        return x, y, width, height

    def get_product_positions(self, available_height, position_style=None):
        """
        Get product positions for collage layout

        Args:
            available_height: Height available for products
            position_style: 'clustered', 'scattered', or 'grid'

        Returns:
            List of (x, y, size, rotation) tuples
        """
        if position_style is None:
            position_style = config.ACTIVE_PRODUCT_POSITION

        positions = config.PRODUCT_POSITIONS[position_style]
        layout = config.LAYOUTS['collage']

        content_width = self.canvas_width - layout['content_margin']
        content_x_offset = layout['content_margin'] // 2

        result = []
        for x_ratio, y_ratio, size_ratio, rotation in positions:
            size = int(available_height * size_ratio)
            x = content_x_offset + int(content_width * x_ratio)
            y = int(y_ratio * available_height)
            result.append((x, y, size, rotation))

        return result

    def get_icon_positions(self, icon_style=None):
        """
        Get icon positions

        Args:
            icon_style: 'default' or 'corners'

        Returns:
            List of (asset_key, x, y, size, movement_range) tuples
        """
        if icon_style is None:
            icon_style = config.ACTIVE_ICON_POSITION

        positions = config.ICON_POSITIONS[icon_style]
        layout = config.LAYOUTS['collage']
        icon_sizes = layout['icon_sizes']

        result = []
        for asset_key, x, y, movement in positions:
            size = icon_sizes.get(asset_key, 120)
            result.append((asset_key, x, y, size, movement))

        return result

    def calculate_floating_position(self, base_x, base_y, frame, total_frames, movement_range=15):
        """
        Calculate floating animation position

        Args:
            base_x: Base X position
            base_y: Base Y position
            frame: Current frame number
            total_frames: Total frames in animation
            movement_range: Maximum pixel movement

        Returns:
            (x, y) tuple
        """
        progress = (frame / total_frames) * 2 * math.pi
        offset_y = math.sin(progress) * movement_range
        offset_x = math.sin(progress * 0.7) * (movement_range * 0.5)

        return int(base_x + offset_x), int(base_y + offset_y)

    def center_element(self, element_width, element_height, container_width=None, container_height=None):
        """
        Calculate position to center element in container

        Args:
            element_width: Width of element
            element_height: Height of element
            container_width: Container width (canvas if None)
            container_height: Container height (canvas if None)

        Returns:
            (x, y) tuple
        """
        if container_width is None:
            container_width = self.canvas_width
        if container_height is None:
            container_height = self.canvas_height

        x = (container_width - element_width) // 2
        y = (container_height - element_height) // 2

        return x, y

    def center_text_group(self, text_heights, total_spacing, container_height):
        """
        Calculate starting Y position to center a group of text lines

        Args:
            text_heights: List of text heights
            total_spacing: Total spacing between lines
            container_height: Container height

        Returns:
            Starting Y position
        """
        total_height = sum(text_heights) + total_spacing
        return (container_height - total_height) // 2


def create_layout_strategy(strategy_name='default'):
    """
    Factory function to create layout strategies

    Args:
        strategy_name: Name of strategy to use

    Returns:
        LayoutEngine instance with configured strategy
    """
    engine = LayoutEngine(config.IMAGE_WIDTH, config.IMAGE_HEIGHT)

    # Add custom strategies here
    strategies = {
        'default': engine,
        'compact': engine,  # Could customize this
        'spacious': engine,  # Could customize this
    }

    return strategies.get(strategy_name, engine)
