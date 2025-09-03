from .database import get_connection
from datetime import datetime, timedelta, timezone

def get_city_trends(days=30):
    conn = get_connection()
    cur = conn.cursor()
    since = datetime.now(timezone.utc) - timedelta(days=days)
    cur.execute("""
        SELECT city, COUNT(*) as count
        FROM crime_reports
        WHERE published_at >= %s
        GROUP BY city
        ORDER BY count DESC;
    """, (since,))
    trends = {row["city"]: row["count"] for row in cur.fetchall()}
    cur.close()
    conn.close()
    return trends

def get_source_stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT source, COUNT(*) as count
        FROM crime_reports
        GROUP BY source
        ORDER BY count DESC;
    """)
    stats = {row["source"]: row["count"] for row in cur.fetchall()}
    cur.close()
    conn.close()
    return stats

def get_recent_reports(limit=20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT source, title, description, city, published_at, url
        FROM crime_reports
        ORDER BY published_at DESC
        LIMIT %s;
    """, (limit,))
    reports = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return reports

