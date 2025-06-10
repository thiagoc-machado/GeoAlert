def classify_text(text: str) -> str:
    if 'flood' in text.lower():
        return 'Flood'
    return 'General'

def summarize_text(text: str) -> str:
    return text[:100] + '...' if len(text) > 100 else text
