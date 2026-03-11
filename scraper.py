import argparse
import time
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

import config
from utils import extract_product_data

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_page(url: str):
    logging.info(f"Scraping {url}")
    try:
        headers = {'User-Agent': config.USER_AGENT}
        response = requests.get(url, timeout=10, headers=headers)
        # Kiểm tra nếu trang không tồn tại (404)
        if response.status_code == 404:
            logging.warning(f"Page not found: {url}")
            return [], False
            
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve {url}: {e}")
        return [], False

    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('article', class_='product_pod')
    
    # Nếu không tìm thấy sản phẩm nào
    if not products:
        logging.warning(f"Không tìm thấy sản phẩm nào tại {url}.")
        return [], False
        
    parsed_data = []
    for product in products:
        parsed_data.append(extract_product_data(product, url))
        
    return parsed_data, True

def save_to_csv(df: pd.DataFrame, file_path: str):
    """Lưu DF vào CSV file."""
    try:
        df.to_csv(file_path, index=False)
        logging.info(f"Lưu dữ liệu vào CSV thành công: {file_path}")
    except Exception as e:
        logging.error(f"Lỗi khi lưu dữ liệu vào CSV: {e}")

def run_scraper(pages: int, csv_path: str):
    """Điều chỉnh thu thập dữ liệu."""
    all_data = []
    page = 1
    
    # Nếu pages <= 0, tiếp tục đến khi không còn trang nào để thu thập
    max_pages = pages if pages > 0 else float('inf')
    
    while page <= max_pages:
        url = config.BASE_URL.format(page)
        page_data, has_next = scrape_page(url)
        
        if not has_next:
            break
            
        all_data.extend(page_data)
        
        # Delay giữa các yêu cầu
        if page < max_pages:
            time.sleep(config.REQUEST_DELAY)
            
        page += 1

    if not all_data:
        logging.warning("Không có dữ liệu nào được thu thập. Thoát.")
        return

    #Chuyển đổi thành Pandas DataFrame
    df = pd.DataFrame(all_data)
    logging.info(f"Thu thập thành công {len(df)} sản phẩm.")
    
    #Lưu
    if csv_path:
        save_to_csv(df, csv_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A web scraper for product data.")
    
    parser.add_argument(
        '-p', '--pages', 
        type=int, 
        default=-1, 
        help='Number of pages to scrape (default: -1 for all pages)'
    )
    
    parser.add_argument(
        '--csv', 
        type=str, 
        nargs='?', 
        const=config.DEFAULT_CSV_PATH,
        help='Export data to CSV file. Specify a path or use the flag alone for the default path.'
    )

    args = parser.parse_args()

    #Mặc định lưu vào data/products.csv nếu không có đường dẫn riêng
    csv_path = args.csv if args.csv else config.DEFAULT_CSV_PATH
    
    # Nếu đường dẫn riêng không chỉ định thư mục, thêm vào data/
    if csv_path and not os.path.dirname(csv_path):
        csv_path = os.path.join(config.DATA_DIR, csv_path)
    
    run_scraper(args.pages, csv_path)
