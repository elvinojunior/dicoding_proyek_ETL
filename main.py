from utils.extract import fetching_content, extract_products
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_googlesheets, load_to_postgresql

def run_etl():
    #Ekstraksi website
    all_products = []
    base_url = "https://fashion-studio.dicoding.dev/"

    # Scrape halaman 1
    print(f"Scraping halaman 1: ...")
    try:
        html_content = fetching_content(base_url)
        if html_content:
            products = extract_products(html_content)
            all_products.extend(products)
    except Exception as e:
        print(f"Gagal scraping halaman 1: {e}")

    # Scrape halaman 2-50
    for page in range(2, 51):
        url = f"{base_url}page{page}"  # pagination URL
        print(f"Scraping halaman {page}: ...")
        try:
            html_content = fetching_content(url)
            if html_content:
                products = extract_products(html_content)
                all_products.extend(products)
        except Exception as e:
            print(f"Gagal scraping halaman {page}: {e}")

    print(f"\nTotal data terambil: {len(all_products)}")

    # Transformasi data
    if all_products:
        try:
            df_clean = transform_data(all_products)
            print(f"Total data setelah transform: {len(df_clean)}")
        except Exception as e:
            print(f"Gagal transform data: {e}")
            return  # stop ETL kalau gagal transform

    # Load ke CSV
        try:
            load_to_csv(df_clean, 'products.csv')
            print("Data berhasil disimpan ke 'products.csv'")
        except Exception as e:
            print(f"Gagal simpan ke CSV: {e}")

    # Load ke Google Sheets
        try:
            spreadsheet_id = '1p6qJwsLHahcDeUUjdrSWabOSMzFDl5wHOnZH1xspNEM'
            range_name = 'Sheet1!A1' 
            load_to_googlesheets(df_clean, spreadsheet_id, range_name)
        except Exception as e:
            print(f"Gagal simpan ke Google Sheets: {e}")

    # Load ke PostgreSQL
        try:
            load_to_postgresql(df_clean, 'products')
        except Exception as e:
            print(f"Gagal simpan ke PostgreSQL: {e}")

    else:
        print("Tidak ada data yang berhasil diambil.")

if __name__ == "__main__":
    run_etl()