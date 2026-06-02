import unittest
from andCount import count_and_occurrences


class TestAndCounter(unittest.TestCase):
    def test_empty_input(self):
        """Test with an empty string"""
        self.assertEqual(count_and_occurrences(""), 0)
    
    def test_no_ands(self):
        """Test a string with no 'and' occurrences"""
        text = "hello world this is a test"
        self.assertEqual(count_and_occurrences(text), 0)
    
    def test_single_and(self):
        """Test a string with one 'and'"""
        text = "This is a test and it works"
        self.assertEqual(count_and_occurrences(text), 1)
    
    def test_multiple_ands(self):
        """Test a string with multiple 'and' occurrences"""
        text = "This and that and another thing and so on"
        self.assertEqual(count_and_occurrences(text), 3)
    
    def test_case_insensitive(self):
        """Test that 'and' is case-insensitive"""
        text = "And AND aNd"
        self.assertEqual(count_and_occurrences(text), 3)
        
    def test_punctuation(self):
        """Test handling of punctuation around 'and'"""
        text = "Hello, and welcome. This and that, and more"
        self.assertEqual(count_and_occurrences(text), 3)

if __name__ == '__main__':
    unittest.main()