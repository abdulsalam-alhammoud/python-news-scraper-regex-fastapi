import requests
from bs4 import BeautifulSoup
import json
import os
import re

# Dateipfade
CACHE_FILE = "news/cache.json"
SOURCES_FILE = "data/news_sources.json"

# Lade alle Newsquellen aus JSON-Datei
def load_sources():
    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Lade den Cache (falls vorhanden)
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except json.JSONDecodeError:
            print("Ungültiges JSON im Cache wird ignoriert.")
    return {}

# Speichere neuen Cache
def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

# Scrape Headlines für eine einzelne Quelle
def scrape_headlines(source):
    try:
        response = requests.get(source["url"], timeout=10)
        response.raise_for_status()
        html_content = response.text

        headlines = []
        # Use regex if provided, otherwise fallback to BeautifulSoup
        if "headline_regex" in source and source["headline_regex"]:
            # Use re.findall to get all matches
            matches = re.findall(source["headline_regex"], html_content, re.DOTALL)
            for match in matches:
                # If the regex captures groups, join them or take the first one
                if isinstance(match, tuple):
                    headlines.append(" ".join(match).strip())
                else:
                    headlines.append(match.strip())
        else:
            soup = BeautifulSoup(html_content, "html.parser")
            for tag in soup.select(source["headline_selector"]):
                text = tag.get_text(" ", strip=True)
                if text:
                    headlines.append(text)
        return headlines

    except Exception as e:
        print(f"Fehler bei {source['name']}: {e}")
        return []

# Filtere eine Liste von Headlines nach Keyword
def filter_headlines(all_headlines, keyword):
    results = []
    for source, title in all_headlines:
        if re.search(keyword, title, re.IGNORECASE):
            results.append((source, title))
    return results

