import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_csv, load_to_postgresql, load_to_googlesheets

class TestLoadFunctions(unittest.TestCase):

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_load_to_csv_success(self, mock_to_csv):
        df = pd.DataFrame({
                'title': ['Product A','Product B'],
                'price': ['$10', '$20'],
                'rating': ['Rating: 5', 'Rating: 4.5'],
                'colors': ['3', '3'],
                'size': ['M', 'L'],
                'gender': ['Unisex', 'Women']
        })

        load_to_csv(df, 'test.csv')
        mock_to_csv.assert_called_once()

    @patch('utils.load.create_engine')
    @patch('utils.load.pd.DataFrame.to_sql')
    def test_load_to_postgresql_success(self, mock_to_sql, mock_create_engine):
        df = pd.DataFrame({
                'title': ['Product A','Product B'],
                'price': ['$10', '$20'],
                'rating': ['Rating: 5', 'Rating: 4.5'],
                'colors': ['3', '3'],
                'size': ['M', 'L'],
                'gender': ['Unisex', 'Women']
        })

        engine_mock = MagicMock()
        mock_create_engine.return_value = engine_mock
        load_to_postgresql(df, 'test_table')
        mock_to_sql.assert_called_once()

    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.build')
    def test_load_to_googlesheets_success(self, mock_build, mock_creds):
        df = pd.DataFrame({
                'title': ['Product A','Product B'],
                'price': ['$10', '$20'],
                'rating': ['Rating: 5', 'Rating: 4.5'],
                'colors': ['3', '3'],
                'size': ['M', 'L'],
                'gender': ['Unisex', 'Women']
        })

        mock_service = MagicMock()
        mock_sheet = MagicMock()
        mock_service.spreadsheets.return_value = mock_sheet
        mock_build.return_value = mock_service

        load_to_googlesheets(df, 'spreadsheet_id', 'Sheet1!A1')
        mock_build.assert_called_once()

if __name__ == '__main__':
    unittest.main()