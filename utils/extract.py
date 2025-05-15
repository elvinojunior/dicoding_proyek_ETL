import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    #mengambil konten HTML dari URL
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def extract_products(html_content):
    try:
        #ekstrak data produk dari konten HTML
        soup = BeautifulSoup(html_content, "html.parser")
        product_cards = soup.find_all('div', class_='collection-card')
        products = []

        for card in product_cards:
            #judul produk
            title_tag = card.find('h3', class_='product-title')
            title = title_tag.text.strip() if title_tag else 'Unknown Product'

            #harga produk
            price_tag = card.find('div', class_='price-container')
            price = price_tag.text.strip() if price_tag else 'Price Unavailable'

            #rating produk
            rating_tag = card.find('p', string=lambda text: text and 'Rating' in text)
            rating = rating_tag.text.strip() if rating_tag else 'Invalid Rating'

            #warna produk
            colors_tag = card.find('p', string=lambda text: text and 'Colors' in text)
            colors = colors_tag.text.strip() if colors_tag else 'No Color Info'

            #ukuran produk
            size_tag = card.find('p', string=lambda text: text and 'Size' in text)
            size = size_tag.text.strip() if size_tag else 'No Size Info'

            #produk untuk gender
            gender_tag = card.find('p', string=lambda text: text and 'Gender' in text)
            gender = gender_tag.text.strip() if gender_tag else 'No Gender Info'
            
            #timestamp data di ekstraksi
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            products.append({
                'title': title,
                'price': price,
                'rating': rating,
                'colors': colors,
                'size': size,
                'gender': gender,
                'timestamp': timestamp
            })

            #time.sleep(0.5)  # Delay untuk menghindari pemblokiran IP
        return products
    
    except Exception as e:
        raise Exception (f"gagal melakukan ekstraksi data: {e}")