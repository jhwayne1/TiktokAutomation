"""
API and data fetching utilities
"""

import requests
from config import creative_config as config


def fetch_deals(api_url=None, max_deals=None):
    """
    Fetch deals from API

    Args:
        api_url: Optional API URL override
        max_deals: Limit number of deals returned

    Returns:
        List of deal dictionaries
    """
    if api_url is None:
        api_url = config.API_URL

    print(f"Fetching deals from {api_url}...")

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        deals = data.get('deals', [])

        if max_deals:
            deals = deals[:max_deals]

        print(f"  Found {len(deals)} deals")
        return deals

    except Exception as e:
        print(f"Error fetching deals: {e}")
        return []


def calculate_discount_percentage(current_price, original_price):
    """
    Calculate discount percentage

    Args:
        current_price: Discounted price
        original_price: Original price

    Returns:
        Discount percentage (int)
    """
    if original_price == 0:
        return 0

    discount = (1 - (current_price / original_price)) * 100
    return round(discount)


def extract_deal_info(deal):
    """
    Extract relevant information from deal object

    Args:
        deal: Deal dictionary from API

    Returns:
        Dictionary with extracted info
    """
    # Get prices
    current_price = deal.get('current_price', 0)
    best_promo = deal.get('best_promo_code', {})

    if best_promo and best_promo.get('price_after_applied'):
        promo_price = best_promo.get('price_after_applied', 0)
        if promo_price < current_price:
            original_price = current_price
            discount_price = promo_price
        else:
            original_price = current_price * 1.25
            discount_price = current_price
    else:
        discount_price = current_price
        original_price = current_price * 1.25

    discount_percent = calculate_discount_percentage(discount_price, original_price)

    # Extract brand name and apply text transform
    brand = deal.get('brand', 'Unknown')
    transform = config.TEXT_TEMPLATES['individual'].get('text_transform', 'lowercase')

    if transform == 'lowercase':
        brand = brand.lower()
    elif transform == 'uppercase':
        brand = brand.upper()
    elif transform == 'title':
        brand = brand.title()

    return {
        'brand': brand,
        'name': deal.get('name', ''),
        'image_urls': deal.get('image_urls', []),
        'short_id': deal.get('short_id', ''),
        'discount_percent': discount_percent,
        'current_price': current_price,
        'original_price': original_price,
    }


def format_discount_text(discount_percent):
    """
    Format discount text according to template

    Args:
        discount_percent: Discount percentage

    Returns:
        Formatted string
    """
    template = config.TEXT_TEMPLATES['individual']['discount_format']
    return template.format(percent=discount_percent)
