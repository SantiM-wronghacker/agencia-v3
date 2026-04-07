from datetime import datetime, timedelta, timezone


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def parse_iso(date_str: str) -> datetime | None:
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return None


def days_from_now(days: int) -> str:
    return (datetime.utcnow() + timedelta(days=days)).date().isoformat()


def hours_since(iso_timestamp: str) -> float:
    dt = parse_iso(iso_timestamp)
    if not dt:
        return 0.0
    diff = datetime.utcnow() - dt.replace(tzinfo=None)
    return diff.total_seconds() / 3600
