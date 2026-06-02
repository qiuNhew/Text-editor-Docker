"""
Function to count word-palindromes in the provided text.
"""
import re

def count_palindromes(input_text):
    if not input_text:
        return 0

    # Sanitize input to remove HTML tags and convert to lowercase
    sanitized_text = re.sub(r'<.*?>', '', input_text).lower()

    # Replace non-alphabetic characters with spaces
    cleaned_text = ''.join(char if char.isalpha() else ' ' for char in sanitized_text)

    # Split text into words and filter out single-letter words
    words = [word for word in cleaned_text.split() if len(word) > 1]

    # Count palindromes
    palindrome_count = sum(1 for word in words if word == word[::-1])

    return palindrome_count
