import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

from kafka import KafkaProducer


KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
TOPIC = os.getenv("KAFKA_TOPIC", "events")


def now():
    return datetime.now(timezone.utc).isoformat()


def generate_event():
    event_type = random.choice(["page_view", "login", "purchase"])

    payload = {
        "path": random.choice([
            "/",
            "/search",
            "/checkout",
            "/restaurants/123"
        ])
    }

    if event_type == "purchase":
        payload["amount"] = round(random.uniform(10, 200), 2)

    return {
        "schema_version": 1,
        "event_id": f"evt_{uuid.uuid4().hex}",
        "user_id": random.randint(1, 10000),
        "event_type": event_type,
        "occurred_at": now(),
        "payload": payload
    }


producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Producer started... sending events")

while True:

    event = generate_event()

    producer.send(TOPIC, value=event)

    print("sent event:", event["event_type"])

    time.sleep(1)