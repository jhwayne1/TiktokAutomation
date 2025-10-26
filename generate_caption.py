#!/usr/bin/env python3
"""
TikTok Caption Generator
Generates engaging captions for daily deal posts
"""

import requests
import random
from datetime import datetime


# Configuration
API_URL = "https://item-api-rosy.vercel.app/api/deals"


def calculate_discount_percentage(current_price, original_price):
    """Calculate discount percentage using the formula: 1-(discount price / full price) * 100"""
    if original_price == 0:
        return 0
    discount = (1 - (current_price / original_price)) * 100
    return round(discount)


def fetch_deals():
    """Fetch deals from API"""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get('deals', [])
    except Exception as e:
        print(f"Error fetching deals: {e}")
        return []


def get_deal_text(deal):
    """Format a single deal for the caption"""
    brand = deal.get('brand', 'Unknown')
    current_price = deal.get('current_price', 0)

    # Try to get original price from best_promo_code or estimate
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

    return f"{brand} - {discount_percent}% off sitewide"


def generate_caption(deals):
    """Generate a complete caption for the daily deals post"""

    # Opening lines - variety of options
    openings = [
        "Coming at you with some fireee deals today! As always treat yourself to something nice.",
        "Got some great finds today. Hope everyone treats themselves to something nice 😎.",
        "Fresh deals just dropped! Treat yourself to something special today.",
        "New deals alert! Time to grab something nice for yourself.",
        "Daily deal drop! Some amazing finds today - don't sleep on these.",
        "Back with more fire deals! As always, treat yourself well.",
    ]

    # Day-specific additions
    day_of_week = datetime.now().strftime("%A")
    if day_of_week in ["Friday", "Saturday", "Sunday"]:
        weekend_phrases = [
            " Have a great weekend fam.",
            " Enjoy your weekend everyone!",
            " Happy weekend shopping!",
        ]
        opening = random.choice(openings) + random.choice(weekend_phrases)
    else:
        opening = random.choice(openings)

    # Format deals list
    deal_lines = []
    for deal in deals[:7]:  # Limit to first 7 deals
        deal_lines.append(get_deal_text(deal))

    deals_text = "\n".join(deal_lines)

    # Hashtags - rotate between sets
    hashtag_sets = [
        "#shopping #deals #fyp #dealsforyoudays #discounts",
        "#shopping #deals #fyp #fypシ #tiktokshop",
        "#deals #shopping #fyp #discount #savings",
        "#dailydeals #shopping #fyp #discounts #sale",
    ]

    hashtags = random.choice(hashtag_sets)

    # Combine all parts
    caption = f"{opening}\n\n{deals_text}\n\n{hashtags}"

    return caption


def main():
    """Main function to generate and display caption"""
    print("=" * 50)
    print("TikTok Caption Generator")
    print("=" * 50)

    # Fetch deals
    deals = fetch_deals()
    print(f"Found {len(deals)} deals\n")

    if not deals:
        print("No deals found. Exiting.")
        return

    # Generate caption
    caption = generate_caption(deals)

    # Display caption
    print("Generated Caption:")
    print("-" * 50)
    print(caption)
    print("-" * 50)

    # Save to file
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"generated_images/{today}"
    import os
    os.makedirs(output_dir, exist_ok=True)

    caption_file = f"{output_dir}/caption.txt"
    with open(caption_file, 'w') as f:
        f.write(caption)

    print(f"\n✓ Caption saved to: {caption_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()
