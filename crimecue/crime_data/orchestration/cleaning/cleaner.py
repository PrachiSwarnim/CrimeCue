import re
from bs4 import BeautifulSoup

def clean_text(text):
    """Clean text by removing HTML tags, extra spaces, and unwanted characters."""
    if not text:
        return ""
    
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove extra spaces, newlines, tabs
    text = re.sub(r"\s+", " ", text).strip()
    
    # Optional: remove any non-printable characters
    text = re.sub(r"[^\x20-\x7E]", "", text)
    
    return text
