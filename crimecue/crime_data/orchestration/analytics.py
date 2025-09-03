from .database import get_connection
from datetime import datetime, timedelta, timezone
import google.generativeai as genai
import os

# Configure Gemini once
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ai_title(news_text: str) -> str:
    """
    Uses Gemini to generate a short, catchy title for a news item.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Summarize this news into a short, engaging title (max 10 words):\n\n{news_text}"
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "Untitled"
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return " ".join(news_text.split()[:6]) + "..."


def get_city_trends(days=30):
    conn = get_connection()
    # Use DictCursor so rows act like dicts
    cur = conn.cursor()
    since = datetime.now(timezone.utc) - timedelta(days=days)
    cur.execute("""
        SELECT city, COUNT(*) as count
        FROM crime_reports
        WHERE published_at >= %s
        GROUP BY city
        ORDER BY count DESC;
    """, (since,))
    rows = cur.fetchall()
    trends = {row["city"]: row["count"] for row in rows}  # city, count
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
    rows = cur.fetchall()
    stats = {row["source"]: row["count"] for row in rows}  # source, count
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
    rows = cur.fetchall()

    reports = []
    descriptions = []
    for idx, row in enumerate(rows, 1):
        report = {
            "source": row["source"],
            "title": row["title"],
            "description": row["description"],
            "city": row["city"],
            "published_at": row["published_at"],
            "url": row["url"],
        }
        reports.append(report)
        descriptions.append(f"{idx}. {report['description'] or report['title']}")

    # --- Gemini batch call ---
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "Generate short, engaging news titles (max 10 words each) "
            "for the following items. Number them clearly:\n\n"
            + "\n".join(descriptions)
        )
        response = model.generate_content(prompt)
        ai_titles_text = response.text.strip().split("\n")

        # Map generated titles back to reports
        for i, report in enumerate(reports):
            try:
                report["ai_title"] = ai_titles_text[i].split(".", 1)[-1].strip()
            except IndexError:
                report["ai_title"] = report["title"] or "Untitled"
    except Exception as e:
        print(f"[Gemini Error] {e}")
        # Fallback to truncating titles locally
        for report in reports:
            report["ai_title"] = (report["title"] or report["description"][:30]) + "..."

    cur.close()
    conn.close()
    return reports
