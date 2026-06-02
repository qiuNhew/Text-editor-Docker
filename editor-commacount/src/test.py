import unittest
from commaCount import comma_counting

class TestCommaCounter(unittest.TestCase):
    def test_empty_input(self):
        """Test with an empty string"""
        self.assertEqual(comma_counting(""), 0)
    
    def test_no_commas(self):
        """Test a string with no commas"""
        text = "hello world this is a test"
        self.assertEqual(comma_counting(text), 0)
    
    def test_single_comma(self):
        """Test a string with one comma"""
        text = "This is a test, and it works"
        self.assertEqual(comma_counting(text), 1)
    
    def test_multiple_commas(self):
        """Test a string with multiple commas"""
        text = "This, that, and another, thing, and so on"
        self.assertEqual(comma_counting(text), 4)
    
    def test_mixed_characters(self):
        """Test string with mixed characters and commas"""
        text = "Hello, world! 123, test, 456"
        self.assertEqual(comma_counting(text), 3)
    
    def test_special_characters(self):
        """Test handling of special characters"""
        text = "Test,with,special!@#$%^&*()characters,nearby"
        self.assertEqual(comma_counting(text), 3)

if __name__ == '__main__':
    unittest.main()