# utils.py

import re
from urllib.parse import urljoin

def clean_price(price_str: str) -> float:
    if not price_str:
        return 0.0
    
    #Loại bỏ ký tự không phải số và dấu chấm
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def extract_product_data(product_html, base_url: str) -> dict:
    """
    Parses an individual product article from books.toscrape.com
    and returns a dictionary of data.
    """
    data = {}
    
    #Title
    h3_tag = product_html.find('h3')
    if h3_tag and h3_tag.find('a'):
        data['title'] = h3_tag.find('a').get('title', '').strip()
    else:
        data['title'] = "Unknown"
        
    #Price
    price_container = product_html.find('p', class_='price_color')
    if price_container:
        data['price'] = clean_price(price_container.text)
    else:
        data['price'] = 0.0
        
    #Rating
    rating_container = product_html.find('p', class_='star-rating')
    if rating_container:
        classes = rating_container.get('class', [])
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        for c in classes:
            if c in rating_map:
                data['rating'] = rating_map[c]
                break
        else:
            data['rating'] = 0
    else:
        data['rating'] = 0

    #Product URL
    if h3_tag and h3_tag.find('a'):
        product_rel_url = h3_tag.find('a').get('href', '')
        data['product_url'] = urljoin(base_url, product_rel_url)
    else:
        data['product_url'] = ""

    #Image URL
    image_container = product_html.find('div', class_='image_container')
    if image_container:
        img_tag = image_container.find('img')
        if img_tag:
            img_rel_url = img_tag.get('src', '')
            data['image_url'] = urljoin(base_url, img_rel_url)
        else:
            data['image_url'] = ""
    else:
        data['image_url'] = ""

    return data
