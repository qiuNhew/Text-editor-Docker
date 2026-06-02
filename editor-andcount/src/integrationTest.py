import unittest
import requests
import json

class TestAndCountIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test server URL"""
        self.base_url = 'http://localhost:80'  # Adjust if different
    
    def test_successful_request(self):
        """Test a successful request with 'and' in text"""
        params = {'text': 'This is a test and it works'}
        response = requests.get(f'{self.base_url}/', params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['error'])
        self.assertEqual(data['total_ands'], 1)
        self.assertIn('1 \'and\'s', data['message'])
    
    def test_no_ands(self):
        """Test request with no 'and' in text"""
        params = {'text': 'Hello world'}
        response = requests.get(f'{self.base_url}/', params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['error'])
        self.assertEqual(data['total_ands'], 0)
        self.assertIn('0 \'and\'s', data['message'])
    
    def test_empty_input(self):
        """Test request with empty text"""
        params = {'text': ''}
        response = requests.get(f'{self.base_url}/', params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['error'])
        self.assertEqual(data['total_ands'], 0)
    
if __name__ == '__main__':
    unittest.main()