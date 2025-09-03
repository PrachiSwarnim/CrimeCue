from django.shortcuts import render
from .orchestration.analytics import get_city_trends, get_source_stats, get_recent_reports
from crime_data.orchestration.orchestrator import run_pipeline


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
    """Render the live crime map page."""
    return render(request, "crime_data/crime_map.html")
