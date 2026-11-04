import re
from typing import List, Tuple

def search_headlines_with_regex(headlines: List[Tuple[str, str]], pattern: str) -> List[Tuple[str, str]]:
    """
    Sucht in Headlines nach einem Regex-Pattern.
    
    Args:
        headlines: Liste von (source, title) Tupeln
        pattern: Regex-Pattern als String
    
    Returns:
        Liste von (source, title) Tupeln, die dem Pattern entsprechen
    """
    results = []
    try:
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        for source, title in headlines:
            if compiled_pattern.search(title):
                results.append((source, title))
    except re.error as e:
        print(f"Ungültiges Regex-Pattern: {e}")
        return []
    
    return results

def extract_keywords_from_headlines(headlines: List[str], pattern: str) -> List[str]:
    """
    Extrahiert Keywords aus Headlines basierend auf einem Regex-Pattern.
    
    Args:
        headlines: Liste von Headlines
        pattern: Regex-Pattern mit Capturing Groups
    
    Returns:
        Liste der extrahierten Keywords
    """
    keywords = []
    try:
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        for headline in headlines:
            matches = compiled_pattern.findall(headline)
            if matches:
                if isinstance(matches[0], tuple):
                    # Wenn mehrere Capturing Groups vorhanden sind
                    keywords.extend([" ".join(match) for match in matches])
                else:
                    # Wenn nur eine Capturing Group vorhanden ist
                    keywords.extend(matches)
    except re.error as e:
        print(f"Ungültiges Regex-Pattern: {e}")
        return []
    
    return keywords

def validate_regex_pattern(pattern: str) -> bool:
    """
    Validiert ein Regex-Pattern.
    
    Args:
        pattern: Regex-Pattern als String
    
    Returns:
        True wenn das Pattern gültig ist, False sonst
    """
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False

def clean_headline_text(text: str) -> str:
    """
    Bereinigt Headlines von HTML-Tags und überflüssigen Zeichen.
    
    Args:
        text: Roher Headline-Text
    
    Returns:
        Bereinigter Text
    """
    # Entferne HTML-Tags
    text = re.sub(r'<[^>]+>', '', text)
    # Entferne mehrfache Leerzeichen
    text = re.sub(r'\s+', ' ', text)
    # Entferne führende und nachfolgende Leerzeichen
    text = text.strip()
    return text
