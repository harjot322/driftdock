import os
import time
from datetime import datetime

import psycopg2
import redis

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
WORKER_VERSION = os.getenv("WORKER_VERSION", "dev")


def db_conn():
    return psycopg2.connect(DATABASE_URL)


def redis_conn():
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


def update_status(event_id, status):
    with db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE events SET status = %s, updated_at = %s WHERE id = %s",
                (status, datetime.utcnow(), event_id),
            )
            conn.commit()


def process_event(event_id):
    update_status(event_id, f"processed:{WORKER_VERSION}")
    time.sleep(0.2)


def main():
    r = redis_conn()
    while True:
        item = r.blpop("driftdock:events", timeout=5)
        if not item:
            continue
        _, event_id = item
        try:
            process_event(int(event_id))
        except Exception:
            update_status(int(event_id), "failed")


if __name__ == "__main__":
    retries = 10
    while retries:
        try:
            db_conn().close()
            redis_conn().ping()
            break
        except Exception:
            retries -= 1
            time.sleep(1)
    main()
