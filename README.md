# Product Scraper

## Description
A Python tool to scrape product data from books.toscrape.com and export to CSV.

## Requirements
- Python 3.8+
- See requirements.txt for dependencies

## Installation
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```bash
python scraper.py
```

## Configuration
Edit `config.py` to change:
- Number of pages
- Delay between requests

## How to run
Use terminal and run
python scraper.py (scrape all products)
# Scrape specific number of pages
python scraper.py -p 5
# Save to custom CSV path
python scraper.py -p 2 --csv my_data.csv


## Output
- CSV file: `data/products.csv`
- Contains [X] products scraped from books.toscrape.com

## Challenges & Solutions
[Describe any difficulties, e.g., handling dynamic content, anti-scraping measures]

## Time Spent
Approximately [X] hours