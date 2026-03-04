CREATE TABLE IF NOT EXISTS events_raw (
  event_id TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL,
  event_type TEXT NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL,
  payload JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_time
ON events_raw (occurred_at);