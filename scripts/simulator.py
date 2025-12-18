import json
import random
import time
import urllib.request

TARGET = "http://gateway/events"

TYPES = ["signup", "checkout", "search", "refund", "alert"]


def send_event():
    payload = {
        "type": random.choice(TYPES),
        "payload": {"value": random.randint(1, 1000)},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(TARGET, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=2) as resp:
            return resp.status
    except Exception:
        return None


def main():
    while True:
        status = send_event()
        print(f"event status={status}")
        time.sleep(0.3)


if __name__ == "__main__":
    main()
