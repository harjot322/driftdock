import json
import os
import time
from datetime import datetime

import psycopg2
import redis
from flask import Flask, jsonify, request

APP_VERSION = os.getenv("APP_VERSION", "dev")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

app = Flask(__name__)
_schema_ready = False


def db_conn():
    return psycopg2.connect(DATABASE_URL)


def redis_conn():
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


def ensure_schema():
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    type TEXT NOT NULL,
                    payload JSONB NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                )
                """
            )
            conn.commit()


def insert_event(event_type, payload):
    now = datetime.utcnow()
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO events (type, payload, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (event_type, json.dumps(payload), "queued", now, now),
            )
            event_id = cur.fetchone()[0]
            conn.commit()
            return event_id


def fetch_event(event_id):
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, type, payload, status, created_at, updated_at FROM events WHERE id = %s",
                (event_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "id": row[0],
                "type": row[1],
                "payload": row[2],
                "status": row[3],
                "created_at": row[4].isoformat() + "Z",
                "updated_at": row[5].isoformat() + "Z",
            }


def stats():
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT status, COUNT(*) FROM events GROUP BY status")
            rows = cur.fetchall()
            return {status: count for status, count in rows}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": APP_VERSION})


@app.route("/events", methods=["POST"])
def create_event():
    payload = request.get_json(silent=True) or {}
    event_type = payload.get("type", "unknown")
    event_payload = payload.get("payload", {})

    event_id = insert_event(event_type, event_payload)
    r = redis_conn()
    r.rpush("driftdock:events", event_id)

    return jsonify({"id": event_id, "status": "queued", "version": APP_VERSION})


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = fetch_event(event_id)
    if not event:
        return jsonify({"error": "not found"}), 404
    return jsonify(event)


@app.route("/stats", methods=["GET"])
def get_stats():
    return jsonify({"version": APP_VERSION, "stats": stats()})


@app.before_request
def init_once():
    global _schema_ready
    if _schema_ready:
        return
    retries = 10
    while retries:
        try:
            ensure_schema()
            _schema_ready = True
            return
        except Exception:
            retries -= 1
            time.sleep(1)
    raise RuntimeError("database unavailable")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
