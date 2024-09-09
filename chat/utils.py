# utils.py
def summarize_text(text):
    words = text.split()
    return ' '.join(words[:10]) + ('...' if len(words) > 10 else '')
