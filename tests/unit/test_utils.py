"""Tests for tools/utils/files.py and tools/utils/dates.py."""
from __future__ import annotations

from pathlib import Path

import pytest

from tools.utils.files import read_file, write_file, list_files
from tools.utils.dates import now_iso, parse_iso, days_from_now, hours_since


# ---------------------------------------------------------------------------
# files.py
# ---------------------------------------------------------------------------

def test_read_file_existing(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hola mundo", encoding="utf-8")
    result = read_file(str(f))
    assert result == "hola mundo"


def test_read_file_pathlib(tmp_path):
    f = tmp_path / "pathlib.txt"
    f.write_text("desde pathlib", encoding="utf-8")
    result = read_file(f)
    assert result == "desde pathlib"


def test_read_file_nonexistent_returns_none(tmp_path):
    result = read_file(str(tmp_path / "no_existe.txt"))
    assert result is None


def test_write_file_creates_file(tmp_path):
    path = tmp_path / "output.txt"
    success = write_file(str(path), "contenido escrito")
    assert success is True
    assert path.read_text(encoding="utf-8") == "contenido escrito"


def test_write_file_creates_parent_dirs(tmp_path):
    path = tmp_path / "sub" / "deep" / "archivo.txt"
    success = write_file(path, "deep content")
    assert success is True
    assert path.exists()


def test_write_file_pathlib_path(tmp_path):
    path = tmp_path / "pathlib_write.txt"
    success = write_file(path, "via pathlib")
    assert success is True
    assert path.read_text() == "via pathlib"


def test_write_file_returns_false_on_error(tmp_path):
    # Try to write to a path that is actually a directory
    bad_path = tmp_path  # tmp_path is a dir, not a file
    result = write_file(bad_path, "data")
    assert result is False


def test_list_files_no_extension(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.py").write_text("b")
    files = list_files(tmp_path)
    names = [f.name for f in files]
    assert "a.txt" in names
    assert "b.py" in names


def test_list_files_with_extension(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.py").write_text("b")
    (tmp_path / "c.txt").write_text("c")
    files = list_files(tmp_path, ".txt")
    names = [f.name for f in files]
    assert "a.txt" in names
    assert "c.txt" in names
    assert "b.py" not in names


def test_list_files_nonexistent_directory_returns_empty():
    result = list_files("/ruta/que/no/existe/jamas")
    assert result == []


def test_list_files_recursion(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "deep.txt").write_text("deep")
    files = list_files(tmp_path, ".txt")
    names = [f.name for f in files]
    assert "deep.txt" in names


# ---------------------------------------------------------------------------
# dates.py
# ---------------------------------------------------------------------------

def test_now_iso_returns_string():
    result = now_iso()
    assert isinstance(result, str)
    assert "T" in result  # ISO format has T separator


def test_now_iso_parseable():
    result = now_iso()
    # Should be parseable back
    from datetime import datetime
    dt = datetime.fromisoformat(result)
    assert dt is not None


def test_parse_iso_valid_date():
    result = parse_iso("2026-01-15T10:30:00")
    assert result is not None
    assert result.year == 2026
    assert result.month == 1
    assert result.day == 15


def test_parse_iso_invalid_returns_none():
    result = parse_iso("not-a-date")
    assert result is None


def test_parse_iso_empty_string_returns_none():
    result = parse_iso("")
    assert result is None


def test_days_from_now_positive():
    result = days_from_now(30)
    assert isinstance(result, str)
    # Should be a valid date in YYYY-MM-DD format
    from datetime import date
    dt = date.fromisoformat(result)
    from datetime import datetime
    delta = dt - datetime.utcnow().date()
    assert 28 <= delta.days <= 31  # Allow for date boundary crossing


def test_days_from_now_zero():
    result = days_from_now(0)
    from datetime import datetime
    today = datetime.utcnow().date().isoformat()
    assert result == today


def test_days_from_now_negative():
    result = days_from_now(-7)
    assert isinstance(result, str)
    from datetime import date
    dt = date.fromisoformat(result)
    from datetime import datetime
    delta = datetime.utcnow().date() - dt
    assert 6 <= delta.days <= 8


def test_hours_since_returns_float():
    # Use a timestamp 2 hours ago
    from datetime import datetime, timedelta
    two_hours_ago = (datetime.utcnow() - timedelta(hours=2)).isoformat()
    result = hours_since(two_hours_ago)
    assert isinstance(result, float)
    assert 1.9 <= result <= 2.1


def test_hours_since_invalid_returns_zero():
    result = hours_since("invalid-timestamp")
    assert result == 0.0


def test_hours_since_empty_returns_zero():
    result = hours_since("")
    assert result == 0.0
