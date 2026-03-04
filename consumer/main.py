import json
import os
import time
from datetime import datetime

import psycopg2
from kafka import KafkaConsumer


KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
TOPIC = os.getenv("KAFKA_TOPIC", "events")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "eventflow-consumers")

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
            print(f"[consumer] waiting for postgres: {e}")
            time.sleep(2)


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def main():
    pg = connect_pg()
    cur = pg.cursor()

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id=GROUP_ID,
        enable_auto_commit=False,     # commit only after DB write
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    insert_sql = """
        INSERT INTO events_raw (event_id, user_id, event_type, occurred_at, payload)
        VALUES (%s, %s, %s, %s, %s::jsonb)
        ON CONFLICT (event_id) DO NOTHING
    """

    processed = 0
    last_log = time.time()

    print(f"[consumer] started topic={TOPIC} kafka={KAFKA_SERVER} db=eventflow")

    for msg in consumer:
        evt = msg.value
        try:
            cur.execute(
                insert_sql,
                (
                    evt["event_id"],
                    int(evt["user_id"]),
                    evt["event_type"],
                    parse_ts(evt["occurred_at"]),
                    json.dumps(evt["payload"]),
                ),
            )
            consumer.commit()  # safe: commit offset after durable write
            processed += 1
        except Exception as e:
            print(f"[consumer] error event_id={evt.get('event_id')}: {e}")
            # no commit -> message will be retried (at-least-once)

        if time.time() - last_log >= 5:
            print(f"[consumer] processed={processed}")
            last_log = time.time()


if __name__ == "__main__":
    main()