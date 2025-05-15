import pandas as pd

# Asumsi nilai tukar 1 USD = 16.000 IDR
EXCHANGE_RATE = 16000

def transform_data(products):
    # Convert list of dict to DataFrame dulu
    df = pd.DataFrame(products)

    # Hapus data invalid title
    df = df[df["title"] != "Unknown Product"]

    # Hapus data rating tidak valid
    df = df[~df["rating"].str.contains("Invalid Rating | Not Rated")]

    # Konversi Price ke rupiah
    def convert_price(price):
        if "Price Unavailable" in price:
            return None
        price_value = float(price.replace("$", "").replace(",", ""))
        return float(price_value * EXCHANGE_RATE)

    df["price"] = df["price"].apply(convert_price)

    # Konversi Rating ke float
    df["rating"] = df["rating"].str.extract(r'(\d+(\.\d+)?)')[0].astype(float)

    # Ambil angka dari Colors
    df["colors"] = df["colors"].str.extract(r'(\d+)')[0].astype(int)

    # Bersihkan Size & Gender
    df["size"] = df["size"].str.replace("Size: ", "", regex=False)
    df["gender"] = df["gender"].str.replace("Gender: ", "", regex=False)

    # Hapus nilai null
    df.dropna(inplace=True)

    # Hapus duplikat
    df.drop_duplicates(inplace=True)

    return df