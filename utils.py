from datetime import datetime, timezone
import uuid


def pr(*args):
    print(*args, end="\n\n")


def gen_uuid():
    u = str(uuid.uuid4())
    return u


def ts():
    current_time = datetime.now(timezone.utc)
    timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
    return timestamp
