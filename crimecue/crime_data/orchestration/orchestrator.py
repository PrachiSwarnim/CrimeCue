import os
import sys
import django
import time
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Add project root to Python path (Windows-friendly)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crimecue.settings")
django.setup()

# Imports from orchestration
from crime_data.orchestration.fetcher import fetch_all
from crime_data.orchestration.cleaning.preprocess import preprocess_all
from crime_data.orchestration.database import (
    create_tables,
    insert_reports_batch,
    load_existing_reports,
    log_pipeline_run
)

# WebSocket setup
channel_layer = get_channel_layer()


def send_ws_notification(report):
    """Send a single crime report to connected WebSocket clients."""
    async_to_sync(channel_layer.group_send)(
        "crimes",
        {
            "type": "send_crime",
            "crime": report
        }
    )


def run_pipeline():
    """Fetch, clean, store, notify, and log crime reports."""
    print("[Orchestrator] Starting pipeline...")
    
    # Ensure DB tables exist
    create_tables()

    # Load existing reports to avoid duplicates
    existing_reports = load_existing_reports()

    # Fetch raw data from sources
    raw_data = fetch_all()

    # Preprocess & clean all reports
    cleaned_reports = preprocess_all(raw_data)

    # Filter out already existing reports
    new_reports = [
        r for r in cleaned_reports
        if (r["source"], r["title"]) not in existing_reports
    ]

    # Insert new reports in batch
    inserted_count = insert_reports_batch(new_reports)

    # Send WS notifications for each new report
    for report in new_reports:
        send_ws_notification({
            "source": report["source"],
            "title": report["title"],
            "description": report["description"],
            "url": report.get("url", ""),
            "city": report["city"],
            "published_at": str(report["published_at"])
        })

    # Log pipeline run per source
    sources = set(r["source"] for r in new_reports)
    for source in sources:
        source_count = len([r for r in new_reports if r["source"] == source])
        log_pipeline_run(source, source_count)

    print(f"[Orchestrator] Pipeline completed. {inserted_count} new reports added.\n")


if __name__ == "__main__":
    while True:
        try:
            run_pipeline()
        except Exception as e:
            print(f"[Orchestrator] Error: {e}")
        print("[Orchestrator] Sleeping for 1 hour...")
        time.sleep(3600)
