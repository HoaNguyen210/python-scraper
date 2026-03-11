# config.py

import os

# Base URL to scrape (Using Books to Scrape as a safe default)
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Delay between requests (in seconds)
REQUEST_DELAY = 1.0

# Number of pages to scrape (can be overridden by CLI or set to none to scrape all)
DEFAULT_NUM_PAGES = 1

# Output paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DEFAULT_CSV_PATH = os.path.join(DATA_DIR, 'products.csv')


# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
