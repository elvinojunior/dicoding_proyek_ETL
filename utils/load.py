from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import pandas as pd

def load_to_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
        print(f"Berhasil simpan ke {filename}")
    except Exception as e:
        print(f"Gagal simpan ke CSV: {e}")


def load_to_googlesheets(df, spreadsheet_id, range_name):
    try:
        # Load credentials dari file service account JSON
        creds = Credentials.from_service_account_file('credential-googlesheets.json')
        
        # Build service untuk Google Sheets API
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Convert DataFrame ke list of lists
        values = [df.columns.tolist()] + df.values.tolist()  # include header
        
        body = {
            'values': values
        }
        
        # Update ke Google Sheets
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Berhasil upload ke Google Sheets : {result.get('updatedCells')}")

    except Exception as e:
        print(f"Gagal upload ke Google Sheets: {e}")

def load_to_postgresql(df, table_name):
    try:
        # Sesuaikan konfigurasi PostgreSQL Anda
        username = 'developer'
        password = 'developer'
        host = 'localhost'
        port = '5432'
        database = 'fashion'

        # Buat engine SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

        # Simpan ke database (replace jika sudah ada)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL table '{table_name}'.")

    except Exception as e:
        print(f"Gagal menyimpan ke PostgreSQL: {e}")