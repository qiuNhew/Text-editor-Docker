"""
Function to count commas in the provided text.
"""

def comma_counting(text):
    # Check for empty input
    if not text:
        return 0

    # Clean the text to keep only letters and convert to lowercase
    processed_text = ''.join(character for character in text if character.isalpha() or character == ',').lower()

    # Character to count
    comma_char = ','
    comma_count = processed_text.count(comma_char)

    return comma_count
