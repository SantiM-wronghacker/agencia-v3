from pathlib import Path


def read_file(path: str | Path) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        return None


def write_file(path: str | Path, content: str) -> bool:
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return True
    except Exception:
        return False


def list_files(directory: str | Path, extension: str = None) -> list[Path]:
    try:
        p = Path(directory)
        if extension:
            return list(p.rglob(f"*{extension}"))
        return list(p.rglob("*"))
    except Exception:
        return []
