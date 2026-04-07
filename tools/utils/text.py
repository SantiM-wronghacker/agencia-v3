import json
import re


def truncate(text: str, max_chars: int, suffix: str = "...") -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - len(suffix)] + suffix


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def format_list(items: list[str], prefix: str = "- ") -> str:
    return "\n".join(f"{prefix}{item}" for item in items)


def extract_json(text: str) -> dict | None:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            return None
    return None
