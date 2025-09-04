from .cleaner import clean_text
from .utils import normalize_timestamp
import re
import os

# Optional: Gemini API (only if fallback is enabled)
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Simple regex-based city matcher (expand this list)
CITY_LIST = [
    "Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru", "Hyderabad",
    "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur",
    "Patna", "Bhopal", "Indore", "Thane", "Surat", "Varanasi", "Ranchi",
    "Guwahati", "Chandigarh", "Noida", "Gurgaon"
]
CITY_PATTERN = re.compile(r"\b(" + "|".join(CITY_LIST) + r")\b", re.IGNORECASE)


def extract_city_from_text(title, description):
    """
    Try to extract city from title/description using regex.
    """
    text = f"{title} {description}"
    match = CITY_PATTERN.search(text)
    if match:
        return match.group(0)
    return None


def extract_city_with_gemini(title, description):
    """
    Use Gemini to extract the most likely city if regex fails.
    """
    prompt = f"""
    Extract the city mentioned in the following news headline/description.
    If no city is mentioned, respond only with "Unknown".

    Title: {title}
    Description: {description}
    """
    try:
        response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
        city = response.text.strip()
        if city and city.lower() != "unknown":
            return city
    except Exception as e:
        print(f"[City Extraction] Gemini fallback failed: {e}")
    return "Unknown"


def enrich_report(report, source, use_gemini=True):
    """
    Normalize and enrich a single report.
    """
    if not isinstance(report, dict):
        report = {"title": str(report), "description": "", "url": "", "published_at": None}
    
    title = clean_text(report.get("title", ""))
    description = clean_text(report.get("description", ""))
    url = report.get("url", "").strip()
    published_at = normalize_timestamp(report.get("published_at"))

    # First try regex-based city extraction
    city = extract_city_from_text(title, description)

    # If regex fails, try Gemini (optional)
    if not city and use_gemini:
        city = extract_city_with_gemini(title, description)

    if not city:
        city = "Unknown"
    
    return {
        "source": source,
        "title": title,
        "description": description,
        "url": url,
        "city": city,
        "published_at": published_at
    }


def preprocess_all(raw_data, use_gemini=True):
    """
    Process all fetched reports.
    Input: {source: [report1, report2, ...]}
    Output: list of cleaned & enriched reports
    """
    all_reports = []
    for source, items in raw_data.items():
        for item in items:
            enriched = enrich_report(item, source, use_gemini=use_gemini)
            if enriched["title"]:  # Skip empty titles
                all_reports.append(enriched)
    return all_reports
