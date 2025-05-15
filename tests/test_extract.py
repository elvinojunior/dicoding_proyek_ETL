import unittest
from unittest.mock import patch, Mock
from utils.extract import fetching_content, extract_products

class TestExtractFunctions(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_fetching_content_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html></html>'
        mock_get.return_value = mock_response

        result = fetching_content("https://fashion-studio.dicoding.dev/")
        self.assertEqual(result, b'<html></html>')

    @patch('utils.extract.requests.get')
    def test_fetching_content_failure(self, mock_get):
        mock_get.side_effect = Exception("Request error")
        with self.assertRaises(Exception) as context:
            fetching_content("https://fashion-studio.dicoding.dev/")
        self.assertIn("Request error", str(context.exception))

    def test_extract_products_success(self):
        html_content = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">product A</h3>
                    <div class="price-container">$20</div>
                    <p>Rating: 5/5 </p>
                    <p>Colors: 3 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Unisex</p>
                </div>
            </body>
        </html>
        """
        result = extract_products(html_content)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('title', result[0])
        self.assertEqual(result[0]['title'], 'product A')

    def test_extract_products_empty_html(self):
        result = extract_products("<html></html>")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()