"""
A simple function to count vowels in a text.
"""

def count_vowels(text):
    if not text:
        return 0, {}

    # Remove non-alphabetic characters and convert to lowercase
    text = ''.join(char for char in text if char.isalpha()).lower()

    vowels = 'aeiou'
    vowel_counts = {vowel: text.count(vowel) for vowel in vowels}
    total_count = sum(vowel_counts.values())

    return total_count, vowel_counts

