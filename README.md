# News Scraper 2.0 - Regex Edition

Ein moderner News-Scraper mit FastAPI und regulären Ausdrücken für die Extraktion und Suche von Nachrichtenschlagzeilen.

## Features

### Scraping-Funktionalität
- **Regex-basierte Extraktion**: Headlines werden direkt mit regulären Ausdrücken aus dem HTML-Code extrahiert
- **Fallback auf CSS-Selektoren**: Unterstützung für traditionelle CSS-Selektoren als Alternative
- **Mehrere Nachrichtenquellen**: Konfigurierbare Quellen über JSON-Datei
- **Caching**: Automatisches Zwischenspeichern der Ergebnisse

### Suchfunktionalität
- **Regex-Suche**: Erweiterte Suche mit regulären Ausdrücken
- **Textsuche**: Einfache Textsuche als Alternative
- **Pattern-Validierung**: Automatische Überprüfung der Regex-Patterns
- **Keyword-Extraktion**: Extraktion spezifischer Keywords aus Headlines

### Web-Interface
- **Modernes HTML-Frontend**: Responsive Design mit CSS3
- **Interaktive Suche**: Live-Suche mit Regex-Unterstützung
- **Quellenverwaltung**: Hinzufügen und Löschen von Nachrichtenquellen
- **CSV-Export**: Export aller Headlines als CSV-Datei

### API-Endpunkte
- `GET /sources` - Alle konfigurierten Quellen abrufen
- `POST /sources` - Neue Quelle hinzufügen
- `DELETE /sources/{id}` - Quelle löschen
- `POST /scrape` - Alle Quellen scrapen
- `GET /headlines` - Alle Headlines abrufen
- `GET /search` - Suche in Headlines (mit Regex-Option)
- `GET /export` - CSV-Export
- `GET /validate-regex` - Regex-Pattern validieren

## Installation

### Voraussetzungen
- Python 3.11+
- pip

### Setup
1. Repository klonen oder Dateien herunterladen
2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

### Starten
```bash
uvicorn main:app --reload
```

Die Anwendung ist dann unter `http://localhost:8000` erreichbar.

## Konfiguration

### Nachrichtenquellen
Quellen werden in `data/news_sources.json` konfiguriert:

```json
{
  "id": "example",
  "name": "Beispiel-Quelle",
  "url": "https://example.com/news",
  "headline_selector": "h2.headline",  // Optional: CSS-Selector
  "headline_regex": "<h2[^>]*>(.*?)</h2>",  // Optional: Regex-Pattern
  "enabled": true
}
```

**Wichtig**: Entweder `headline_selector` oder `headline_regex` muss angegeben werden.

## Regex-Beispiele

### Häufige Patterns
- `\\b(KI|AI|Künstliche Intelligenz)\\b` - KI-bezogene Begriffe
- `\\d{4}` - Vierstellige Zahlen (Jahre)
- `(?i)bitcoin|crypto` - Bitcoin/Crypto (case-insensitive)
- `^.{0,50}$` - Headlines mit maximal 50 Zeichen

### Für Headlines-Extraktion
- `<h[1-6][^>]*>(.*?)</h[1-6]>` - Alle Überschriften-Tags
- `<a[^>]*class="[^"]*headline[^"]*"[^>]*>(.*?)</a>` - Links mit "headline" in der Klasse
- `<span[^>]*class="title"[^>]*>(.*?)</span>` - Spans mit Klasse "title"

## Projektstruktur

```
news_scraper2.0/
├── main.py              # FastAPI-Anwendung
├── scraper.py           # Scraping-Logik
├── regex_utils.py       # Regex-Hilfsfunktionen
├── requirements.txt     # Python-Abhängigkeiten
├── data/
│   └── news_sources.json # Quellenkonfiguration
├── news/
│   └── cache.json       # Cache-Datei
└── template/
    └── index.html       # HTML-Frontend
```

## Verwendung

### Web-Interface
1. Browser öffnen: `http://localhost:8000`
2. "Alle Quellen scrapen" klicken
3. Suche verwenden:
   - Normale Textsuche: Suchbegriff eingeben
   - Regex-Suche: Checkbox aktivieren und Pattern eingeben

### API-Verwendung
```python
import requests

# Headlines scrapen
response = requests.post('http://localhost:8000/scrape')

# Suche mit Regex
response = requests.get('http://localhost:8000/search?query=KI|AI&use_regex=true')

# Neue Quelle hinzufügen
source_data = {
    "url": "https://example.com",
    "headline_regex": "<h2>(.*?)</h2>",
    "enabled": True
}
response = requests.post('http://localhost:8000/sources', json=source_data)
```

## Entwicklung

### Neue Features hinzufügen
1. API-Endpunkte in `main.py` erweitern
2. Scraping-Logik in `scraper.py` anpassen
3. Regex-Funktionen in `regex_utils.py` hinzufügen
4. Frontend in `template/index.html` aktualisieren

### Testing
- Lokaler Test: Server starten und Browser verwenden
- API-Tests: Mit curl oder Postman
- Regex-Tests: `/validate-regex` Endpunkt verwenden

## Troubleshooting

### Häufige Probleme
1. **Keine Headlines gefunden**: 
   - CSS-Selector oder Regex-Pattern überprüfen
   - Website-Struktur hat sich geändert

2. **Regex-Fehler**:
   - Pattern mit `/validate-regex` testen
   - Escaping von Sonderzeichen beachten

3. **Scraping-Fehler**:
   - Internetverbindung prüfen
   - Website-Verfügbarkeit testen
   - Timeout-Einstellungen anpassen

### Logs
Fehler werden in der Konsole ausgegeben. Bei Problemen:
1. Server-Logs überprüfen
2. Browser-Entwicklertools verwenden
3. Network-Tab für API-Aufrufe prüfen

## Lizenz

Dieses Projekt wurde für Bildungszwecke entwickelt.

## Autoren

- yazan shreteh
- rafi abdin
- mirand gashi
- abdulsalam alhammoud
