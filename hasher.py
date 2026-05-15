import hashlib
from datetime import datetime


def generate_row_hash(row, columns):
    combined = "|".join(str(row[col]) for col in columns if col in row)
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def update_row_hash(row, columns):
    row["row_hash"] = generate_row_hash(row, columns)
    row["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return row


def verify_row_hash(row, columns):
    stored_hash = str(row.get("row_hash", "")).strip()
    current_hash = generate_row_hash(row, columns)
    return stored_hash == current_hash