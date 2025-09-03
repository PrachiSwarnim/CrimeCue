from django.shortcuts import render
from .orchestration.analytics import get_city_trends, get_source_stats, get_recent_reports


def home(request):
    return render(request, "crime_data/home.html")
def dashboard(request):
    trends = get_city_trends(days=30)
    sources = get_source_stats()
    recent = get_recent_reports(limit=30)

    context = {
        "city_trends": trends,
        "source_stats": sources,
        "recent_reports": recent   
    }
    return render(request, "crime_data/dashboard.html", context)

def crime_map(request):
    """Render the live crime map page."""
    return render(request, "crime_data/crime_map.html")