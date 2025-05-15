import unittest
from utils.transform import transform_data

class TestTransformFunctions(unittest.TestCase):

    def test_transform_data_cleaning(self):
        products = [
            {
                'title': 'Product A',
                'price': '$20',
                'rating': 'Rating: 4.5',
                'colors': '3 Colors',
                'size': 'Size: L',
                'gender': 'Gender: Unisex',
                'timestamp': '2024-05-07 12:00:00'
            },

            {
                'title': 'Unknown Product',
                'price': 'Price Unavailable',
                'rating': 'Invalid Rating',
                'colors': 'Colors: 0',
                'size': 'Size: -',
                'gender': 'Gender: -',
                'timestamp': '2024-05-07 12:00:00'
            }
        ]

        df = transform_data(products)

        self.assertEqual(len(df), 1) 
        self.assertEqual(df.iloc[0]['title'], 'Product A') 
        self.assertEqual(df.iloc[0]['price'], 320000.0)
        self.assertEqual(df.iloc[0]['rating'], 4.5)


if __name__ == '__main__':
    unittest.main()