import os
import time
from datetime import datetime, timedelta, timezone

import psycopg2
from fastapi import FastAPI, Query

app = FastAPI(title="EventFlow API")

POSTGRES_DSN = os.getenv(
    "POSTGRES_DSN",
    "dbname=eventflow user=stream password=stream host=postgres port=5432"
)


def connect_pg():
    while True:
        try:
            conn = psycopg2.connect(POSTGRES_DSN)
            conn.autocommit = True
            return conn
        except Exception as e:
            print(f"[api] waiting for postgres: {e}")
            time.sleep(2)


PG = connect_pg()


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/metrics/pageviews")
def pageviews(window_seconds: int = Query(60, ge=5, le=3600)):
    since = datetime.now(timezone.utc) - timedelta(seconds=window_seconds)

    with PG.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM events_raw
            WHERE event_type = 'page_view'
            AND occurred_at >= %s
            """,
            (since,),
        )

        (count,) = cur.fetchone()

    return {
        "window_seconds": window_seconds,
        "page_views": int(count),
    }