import difflib

def calculate_similarity(text1, text2):
    similarity_ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
    return similarity_ratio

# Example usage
text1 = "The future belongs to those who believe in the beauty of their dreams."
text2 = "The future belong to those who believe in the beauty of their dreams."
similarity = calculate_similarity(text1, text2)
print("Similarity:", similarity)
