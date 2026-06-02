import unittest
from palindromeCount import count_palindromes

class TestPalindromeCounter(unittest.TestCase):
    def test_empty_input(self):
        """Test with an empty string"""
        self.assertEqual(count_palindromes(""), 0)
    
    def test_no_palindromes(self):
        """Test a string with no palindromes"""
        text = "hello world this is a test"
        self.assertEqual(count_palindromes(text), 0)
    
    def test_single_palindrome(self):
        """Test a string with one palindrome"""
        text = "This is a level test"
        self.assertEqual(count_palindromes(text), 1)
    
    def test_multiple_palindromes(self):
        """Test a string with multiple palindromes"""
        text = "level radar madam hello world"
        self.assertEqual(count_palindromes(text), 3)
    
    def test_case_insensitive(self):
        """Test that palindrome detection is case-insensitive"""
        text = "Level Radar Madam"
        self.assertEqual(count_palindromes(text), 3)
    
    def test_html_tags(self):
        """Test handling of HTML tags"""
        text = "This <b>level</b> and <i>radar</i> are palindromes"
        self.assertEqual(count_palindromes(text), 2)
    
    def test_punctuation(self):
        """Test handling of punctuation"""
        text = "Level, radar! Madam? hello world."
        self.assertEqual(count_palindromes(text), 3)
    
    def test_ignore_single_letters(self):
        """Test that single-letter words are ignored"""
        text = "a b c level d e"
        self.assertEqual(count_palindromes(text), 1)

if __name__ == '__main__':
    unittest.main()