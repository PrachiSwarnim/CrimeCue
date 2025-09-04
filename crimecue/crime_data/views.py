from django.shortcuts import render
from .orchestration.analytics import get_city_trends, get_source_stats, get_recent_reports
from crime_data.orchestration.orchestrator import run_pipeline
from .orchestration.database import get_connection

def home(request):
    """Render the home page."""
    return render(request, "crime_data/home.html")

def dashboard(request):
    """Render the dashboard with trends, sources, and recent reports."""
    run_pipeline()
    trends = get_city_trends(days=30)
    sources = get_source_stats()
    recent = get_recent_reports(limit=30)

    # Convert dict keys & values to lists for Chart.js compatibility
    context = {
        "city_trends_labels": list(trends.keys()),
        "city_trends_values": list(trends.values()),
        "source_stats_labels": list(sources.keys()),
        "source_stats_values": list(sources.values()),
        "recent_reports": recent,
    }
    return render(request, "crime_data/dashboard.html", context)


def crime_map(request):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, description, city, url, latitude, longitude
        FROM crime_reports
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        LIMIT 100;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    reports = []
    for r in rows:
        reports.append({
            "title": r["title"],
            "description": r["description"],
            "city": r["city"],
            "url": r["url"],
            "lat": r["latitude"],
            "lng": r["longitude"],
        })

    return render(request, "crime_data/crime_map.html", {
        "crime_reports": json.dumps(reports)
    })