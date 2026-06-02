import unittest
import requests
import json

class TestVowelCountIntegration(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:80'
    
    def test_successful_request(self):
        """Test a successful request with multiple vowels"""
        params = {'text': 'Beautiful language'}
        response = requests.get(f'{self.base_url}/', params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['error'])
        self.assertEqual(data['answer'],9)
        self.assertIn('Contains 9 vowels', data['string'])
        self.assertEqual(data['details'], {'a': 3, 'e': 2, 'i': 1, 'o': 0, 'u': 3})
    
    def test_no_vowels(self):
        """Test request with no vowels"""
        params = {'text': 'rhythm glyphs'}
        response = requests.get(f'{self.base_url}/', params=params)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['error'])
        self.assertEqual(data['answer'], 0)
        self.assertIn('Contains 0 vowels', data['string'])
    
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