# Teammitglieder:
#yazan shreteh
#rafi abdin
#mirand gashi
#abdulsalam alhammoud

from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Query
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import csv
import io

from scraper import (
    load_sources,
    save_cache,
    load_cache,
    scrape_headlines,
    filter_headlines
)
from regex_utils import (
    search_headlines_with_regex,
    extract_keywords_from_headlines,
    validate_regex_pattern
)

# Datei-Konstanten
SOURCES_FILE = "data/news_sources.json"
CACHE_FILE = "news/cache.json"

app = FastAPI(title="News Scraper API", version="2.0")


# Datenmodelle


class SourceInput(BaseModel):
    url: str
    headline_selector: Optional[str] = None
    headline_regex: Optional[str] = None
    enabled: Optional[bool] = True

class Source(SourceInput):
    id: str
    name: str

class Headline(BaseModel):
    source: str
    title: str

class SearchRequest(BaseModel):
    query: str
    use_regex: Optional[bool] = False


# Quellenverwaltung


@app.get("/sources", response_model=List[Source])
def get_sources():
    """Gibt alle konfigurierten Nachrichtenquellen zurück."""
    return load_sources()

@app.post("/sources", response_model=Source, status_code=201)
def add_source(source: SourceInput):
    """Fügt eine neue Nachrichtenquelle hinzu."""
    sources = load_sources()
    new_id = str(uuid.uuid4())
    name = f"Quelle-{len(sources)+1}"
    new_source = {
        "id": new_id,
        "name": name,
        **source.dict()
    }
    sources.append(new_source)
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2, ensure_ascii=False)
    return new_source

@app.delete("/sources/{source_id}", status_code=204)
def delete_source(source_id: str):
    """Löscht eine Nachrichtenquelle."""
    sources = load_sources()
    new_sources = [s for s in sources if s["id"] != source_id]
    if len(new_sources) == len(sources):
        raise HTTPException(status_code=404, detail="Quelle nicht gefunden")
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(new_sources, f, indent=2, ensure_ascii=False)

# Scraping-Funktionen

@app.post("/scrape", response_model=dict)
def scrape_all():
    """Scrapt Headlines von allen aktivierten Quellen."""
    sources = load_sources()
    cache = {}
    for src in sources:
        if src.get("enabled", True):
            headlines = scrape_headlines(src)
            cache[src["name"]] = headlines
    save_cache(cache)
    return {"status": "ok", "sources": list(cache.keys())}

@app.post("/scrape/{source_name}", response_model=List[str])
def scrape_single(source_name: str):
    """Scrapt Headlines von einer einzelnen Quelle."""
    sources = load_sources()
    src = next((s for s in sources if s["name"].lower() == source_name.lower()), None)
    if not src:
        raise HTTPException(status_code=404, detail="Quelle nicht gefunden")
    headlines = scrape_headlines(src)
    cache = load_cache()
    cache[src["name"]] = headlines
    save_cache(cache)
    return headlines

# Headline-Funktionen
@app.get("/headlines", response_model=List[Headline])
def list_all_headlines():
    """Gibt alle gecachten Headlines zurück."""
    cache = load_cache()
    return [{"source": source, "title": title} for source, titles in cache.items() for title in titles]

@app.get("/headlines/{source_name}", response_model=List[Headline])
def list_by_source(source_name: str):
    """Gibt Headlines einer bestimmten Quelle zurück."""
    cache = load_cache()
    if source_name not in cache:
        raise HTTPException(status_code=404, detail="Keine Daten für diese Quelle")
    return [{"source": source_name, "title": title} for title in cache[source_name]]

@app.get("/search", response_model=List[Headline])
def search_headlines(query: str, use_regex: bool = Query(False, description="Verwende Regex für die Suche")):
    """Sucht in Headlines nach einem Suchbegriff oder Regex-Pattern."""
    cache = load_cache()
    all_headlines = []
    for source, titles in cache.items():
        for title in titles:
            all_headlines.append((source, title))
    
    if use_regex:
        if not validate_regex_pattern(query):
            raise HTTPException(status_code=400, detail="Ungültiges Regex-Pattern")
        results = search_headlines_with_regex(all_headlines, query)
    else:
        results = filter_headlines(all_headlines, query)
    
    return [{"source": source, "title": title} for source, title in results]

@app.post("/search", response_model=List[Headline])
def search_headlines_post(search_request: SearchRequest):
    """Sucht in Headlines nach einem Suchbegriff oder Regex-Pattern (POST)."""
    cache = load_cache()
    all_headlines = []
    for source, titles in cache.items():
        for title in titles:
            all_headlines.append((source, title))
    
    if search_request.use_regex:
        if not validate_regex_pattern(search_request.query):
            raise HTTPException(status_code=400, detail="Ungültiges Regex-Pattern")
        results = search_headlines_with_regex(all_headlines, search_request.query)
    else:
        results = filter_headlines(all_headlines, search_request.query)
    
    return [{"source": source, "title": title} for source, title in results]

@app.get("/extract-keywords")
def extract_keywords(pattern: str):
    """Extrahiert Keywords aus Headlines basierend auf einem Regex-Pattern."""
    if not validate_regex_pattern(pattern):
        raise HTTPException(status_code=400, detail="Ungültiges Regex-Pattern")
    
    cache = load_cache()
    all_headlines = []
    for source, titles in cache.items():
        all_headlines.extend(titles)
    
    keywords = extract_keywords_from_headlines(all_headlines, pattern)
    return {"keywords": keywords, "count": len(keywords)}

# CSV-Export

@app.get("/export")
def export_headlines():
    """Exportiert alle Headlines als CSV-Datei."""
    cache = load_cache()
    data = [(source, title) for source, titles in cache.items() for title in titles]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Quelle", "Titel"])
    writer.writerows(data)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"}
    )

# Validierung

@app.get("/validate-regex")
def validate_regex(pattern: str):
    """Validiert ein Regex-Pattern."""
    is_valid = validate_regex_pattern(pattern)
    return {"pattern": pattern, "valid": is_valid}

# Frontend

templates = Jinja2Templates(directory="template")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    """Zeigt die Homepage mit dem HTML-Frontend."""
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
