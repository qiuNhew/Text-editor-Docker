import unittest
import requests
import json

class TestCommaCountIntegration(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:80'
    
    def test_successful_request(self):
        """Test a successful request with commas"""
        params = {'text': 'This is a test, and it works, perfectly'}
        response = requests.get(f'{self.base_url}/', params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['error'])
        self.assertEqual(data['answer'], 2)
        self.assertIn('Contains 2 commas', data['string'])
    
    def test_no_commas(self):
        """Test request with no commas"""
        params = {'text': 'Hello world'}
        response = requests.get(f'{self.base_url}/', params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['error'])
        self.assertEqual(data['answer'], 0)
        self.assertIn('Contains 0 commas', data['string'])
    
    def test_empty_input(self):
        """Test request with empty text"""
        params = {'text': ''}
        response = requests.get(f'{self.base_url}/', params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['error'])
        self.assertEqual(data['answer'], 0)
    
    def test_missing_text_parameter(self):
        """Test request without text parameter"""
        response = requests.get(f'{self.base_url}/')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify the default behavior when no text is provided
        self.assertFalse(data['error'])
        self.assertEqual(data['answer'], 0)

if __name__ == '__main__':
    unittest.main()