# EventFlow

**EventFlow** is a distributed event streaming platform designed to ingest, process, and expose real-time analytics data using a microservice architecture.

The system simulates high-volume user activity events and processes them asynchronously through a Kafka-based event pipeline, storing results in PostgreSQL and exposing analytics metrics through a FastAPI service.

This project demonstrates core backend engineering concepts including event-driven architecture, distributed messaging systems, idempotent processing, and containerized infrastructure.

---

# Architecture

Producer → Kafka → Consumer → PostgreSQL → FastAPI

Components:

• **Producer** – Generates synthetic user events and streams them into Kafka  
• **Kafka Broker** – Handles distributed event messaging and buffering  
• **Consumer Worker** – Processes events and persists them to PostgreSQL  
• **PostgreSQL** – Stores processed event data  
• **FastAPI Service** – Exposes analytics endpoints for querying event metrics  

---

# Tech Stack

### Languages
- Python

### Infrastructure
- Kafka
- Docker Compose

### Backend Services
- FastAPI
- Kafka-Python
- PostgreSQL

### Database
- PostgreSQL

---

# Event Example

Example event produced into Kafka:


{
  "schema_version": 1,
  "event_id": "evt_5d5cfa",
  "user_id": 8421,
  "event_type": "page_view",
  "occurred_at": "2026-03-04T21:03:14Z",
  "payload": {
    "path": "/restaurants/123"
  }
}

---

# Running the System

## 1. Clone the repository

git clone https://github.com/EitanCohen77/EventFlow.git
cd EventFlow

## 2. Start all services

docker compose up --build

This launches:

* Kafka broker

- Zookeeper

- PostgreSQL

- Producer service

- Consumer service

- FastAPI analytics service

# API Endpoints

## Health Check

GET /health

Example:

http://localhost:8000/health

## Page View Metrics

Returns page view counts within a time window.

GET /metrics/pageviews

Example:

http://localhost:8000/metrics/pageviews

Response:

{

    "window_seconds": 60,

    page_views": 42

}

# Future Improvements

- Redis caching layer for analytics queries

- Dead-letter queue for failed event processing

- Load testing and throughput benchmarking

- Horizontal scaling for consumer workers

- Infrastructure deployment using Kubernetes