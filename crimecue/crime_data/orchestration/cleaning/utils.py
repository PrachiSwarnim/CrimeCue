from datetime import datetime

def normalize_timestamp(ts):
    """Convert timestamp string to datetime object."""
    if not ts:
        return datetime.utcnow()
    if isinstance(ts, datetime):
        return ts
    try:
        # Attempt ISO format
        return datetime.fromisoformat(ts)
    except ValueError:
        try:
            # Fallback common formats
            return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.utcnow()  # fallback

def extract_city(source):
    """Get city name from source string."""
    return source.split("_")[0].capitalize()
