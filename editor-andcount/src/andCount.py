"""
Function to count occurrences of the word 'and' in the provided text.
"""
import re

def count_and_occurrences(input_text):
    if not input_text:
        return 0

    sanitized_text = re.sub(r'<.*?>', '', input_text).lower()
    
    cleaned_text = ''.join(char if char.isalnum() else ' ' for char in sanitized_text)
    and_occurrences = re.findall(r'\band\b', cleaned_text)

    return len(and_occurrences)
