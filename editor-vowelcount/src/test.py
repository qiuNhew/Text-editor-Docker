import unittest
from vowelCount import count_vowels

class TestVowelCounter(unittest.TestCase):
    def test_empty_input(self):
        """Test with an empty string"""
        total_count, vowel_details = count_vowels("")
        self.assertEqual(total_count, 0)
        self.assertEqual(vowel_details, {})
    
    def test_no_vowels(self):
        """Test a string with no vowels"""
        text = "rhythm glyphs"
        total_count, vowel_details = count_vowels(text)
        self.assertEqual(total_count, 0)
        self.assertEqual(vowel_details, {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0})
    
    def test_single_vowel(self):
        """Test a string with a single vowel"""
        text = "hello"
        total_count, vowel_details = count_vowels(text)
        self.assertEqual(total_count, 2)
        self.assertEqual(vowel_details, {'a': 0, 'e': 1, 'i': 0, 'o': 1, 'u': 0})
    
    def test_case_insensitive(self):
        """Test that vowel counting is case-insensitive"""
        text = "AeIoU"
        total_count, vowel_details = count_vowels(text)
        self.assertEqual(total_count, 5)
        self.assertEqual(vowel_details, {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1})
    
if __name__ == '__main__':
    unittest.main()