import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "crime_data"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "prachi2973"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def get_connection():
    """Return a PostgreSQL connection with RealDictCursor."""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


def create_tables():
    """Create the main tables if they don't exist."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS crime_reports (
                        id SERIAL PRIMARY KEY,
                        source TEXT NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        url TEXT,
                        city TEXT,
                        published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(source, title)
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS pipeline_log (
                        id SERIAL PRIMARY KEY,
                        run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        source TEXT,
                        new_reports INT,
                        status TEXT
                    );
                """)
        print("[DB] Tables ready")
    except Exception as e:
        print(f"[DB Error] Failed to create tables: {e}")


def insert_reports_batch(reports):
    """
    Insert multiple crime reports into the database.
    Ignores duplicates based on (source, title) uniqueness.
    """
    if not reports:
        return 0

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = """
                    INSERT INTO crime_reports (source, title, description, url, city, published_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (source, title) DO NOTHING;
                """
                data = [
                    (
                        r.get("source"),
                        r.get("title"),
                        r.get("description", ""),
                        r.get("url", ""),
                        r.get("city", ""),
                        r.get("published_at") or datetime.now()
                    )
                    for r in reports
                ]
                cur.executemany(sql, data)
        print(f"[DB] {len(data)} reports inserted successfully")
        return len(data)
    except Exception as e:
        print(f"[DB Error] Failed to insert batch: {e}")
        return 0


def report_exists(source, title):
    """Check if a report already exists."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM crime_reports WHERE source = %s AND title = %s LIMIT 1;",
                    (source, title)
                )
                return cur.fetchone() is not None
    except Exception as e:
        print(f"[DB Error] Failed to check report existence: {e}")
        return False


def log_pipeline_run(source, new_reports, status="success"):
    """Log a single run of the pipeline."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO pipeline_log (source, new_reports, status) VALUES (%s, %s, %s)",
                    (source, new_reports, status)
                )
        print(f"[DB] Pipeline run logged: {source} - {new_reports} new reports")
    except Exception as e:
        print(f"[DB Error] Failed to log pipeline run: {e}")