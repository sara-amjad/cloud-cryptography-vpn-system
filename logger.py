from datetime import datetime

LOG_FILE = "logs/system_log.txt"


def log_event(event_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{event_type}] {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)