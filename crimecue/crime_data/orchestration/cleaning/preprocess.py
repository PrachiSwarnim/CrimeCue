from .cleaner import clean_text
from .utils import normalize_timestamp, extract_city

def enrich_report(report, source):
    """
    Normalize and enrich a single report.
    - Cleans title and description
    - Normalizes timestamp
    - Adds city field
    """
    if not isinstance(report, dict):
        report = {"title": str(report), "description": "", "url": "", "published_at": None}
    
    title = clean_text(report.get("title", ""))
    description = clean_text(report.get("description", ""))
    url = report.get("url", "").strip()
    published_at = normalize_timestamp(report.get("published_at"))
    city = extract_city(source)
    
    return {
        "source": source,
        "title": title,
        "description": description,
        "url": url,
        "city": city,
        "published_at": published_at
    }

def preprocess_all(raw_data):
    """
    Process all fetched reports.
    Input: dictionary {source: [report1, report2, ...]}
    Output: list of cleaned & enriched reports
    """
    all_reports = []
    for source, items in raw_data.items():
        for item in items:
            enriched = enrich_report(item, source)
            # Skip empty titles
            if enriched["title"]:
                all_reports.append(enriched)
    return all_reports
