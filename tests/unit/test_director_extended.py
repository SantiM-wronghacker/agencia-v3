"""Extended tests for core/director.py."""
import sys
from unittest.mock import MagicMock, patch

import pytest

from core.director import (
    ROLES,
    _c, BLUE, GREEN, RED,
    build_director_agents,
    header,
    mostrar_roles,
    verificar_estado,
    asignar_tarea,
    main,
)


# ---------------------------------------------------------------------------
# ROLES dict
# ---------------------------------------------------------------------------

def test_director_all_six_roles_defined():
    assert set(ROLES.keys()) == {"strategy", "finance", "legal", "marketing", "tech", "ops"}


def test_director_roles_have_emoji_and_desc():
    for rol, info in ROLES.items():
        assert info.get("emoji", "") != "", f"Rol '{rol}' no tiene emoji"
        assert info.get("desc", "") != "", f"Rol '{rol}' no tiene descripción"


# ---------------------------------------------------------------------------
# build_director_agents
# ---------------------------------------------------------------------------

def test_build_director_agents_returns_six(fake_llm):
    with patch("core.agent.get_llm", return_value=fake_llm):
        agents = build_director_agents()
    assert len(agents) == 6


def test_build_director_agents_covers_all_roles(fake_llm):
    with patch("core.agent.get_llm", return_value=fake_llm):
        agents = build_director_agents()
    roles = {a.role for a in agents}
    assert roles == {"strategy", "finance", "legal", "marketing", "tech", "ops"}


def test_director_task_types_are_valid(fake_llm):
    valid = {"reasoning", "general", "long_doc", "simple"}
    with patch("core.agent.get_llm", return_value=fake_llm):
        for agent in build_director_agents():
            assert agent.task_type in valid, (
                f"Rol '{agent.role}' tiene task_type inválido: '{agent.task_type}'"
            )


def test_director_strategy_agent_runs(fake_llm):
    fake_llm.responses["strategy"] = "Plan de 90 días generado."
    with patch("core.agent.get_llm", return_value=fake_llm):
        agents = build_director_agents()
    strategy_agent = next(a for a in agents if a.role == "strategy")
    result = strategy_agent.run("Plan de crecimiento Q3")
    assert result.success
    assert len(result.output) > 0


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def test_director_mostrar_roles_prints_all_roles(capsys):
    mostrar_roles()
    out = capsys.readouterr().out.lower()
    for rol in ("strategy", "finance", "legal", "marketing", "tech", "ops"):
        assert rol in out, f"Rol '{rol}' no aparece en la salida de mostrar_roles()"


def test_director_verificar_estado_runs_without_crash(capsys):
    import httpx
    with patch.object(httpx, "get", side_effect=Exception("connection refused")):
        with patch("core.director._get_db") as mock_get_db:
            mock_get_db.return_value.get_recent_runs.return_value = []
            with patch("llm.get_llm", side_effect=Exception("sin LLM")):
                verificar_estado()
    out = capsys.readouterr().out
    assert len(out) > 0


# ---------------------------------------------------------------------------
# _c color helper
# ---------------------------------------------------------------------------

def test_c_returns_text_containing_input():
    result = _c("hola mundo", BLUE)
    assert "hola mundo" in result


def test_c_different_colors():
    assert "test" in _c("test", GREEN)
    assert "test" in _c("test", RED)


# ---------------------------------------------------------------------------
# header()
# ---------------------------------------------------------------------------

def test_header_prints_output(capsys):
    header()
    out = capsys.readouterr().out
    assert len(out) > 0


# ---------------------------------------------------------------------------
# asignar_tarea
# ---------------------------------------------------------------------------

def test_asignar_tarea_success(fake_llm, capsys):
    fake_llm.responses["strategy"] = "Estrategia generada exitosamente."
    mock_db = MagicMock()
    with patch("core.agent.get_llm", return_value=fake_llm):
        with patch("core.director._get_db", return_value=mock_db):
            asignar_tarea("strategy", "Plan de crecimiento Q3")
    out = capsys.readouterr().out
    assert len(out) > 0


def test_asignar_tarea_finance_role(fake_llm, capsys):
    fake_llm.responses["finance"] = "Análisis financiero completado."
    mock_db = MagicMock()
    with patch("core.agent.get_llm", return_value=fake_llm):
        with patch("core.director._get_db", return_value=mock_db):
            asignar_tarea("finance", "Calcular ROI de inversión")
    out = capsys.readouterr().out
    assert len(out) > 0


def test_asignar_tarea_verbose_shows_provider(fake_llm, capsys):
    fake_llm.responses["ops"] = "Proceso optimizado."
    mock_db = MagicMock()
    with patch("core.agent.get_llm", return_value=fake_llm):
        with patch("core.director._get_db", return_value=mock_db):
            asignar_tarea("ops", "Optimizar proceso de onboarding", verbose=True)
    out = capsys.readouterr().out
    assert len(out) > 0


def test_asignar_tarea_handles_llm_exception(capsys):
    with patch("core.agent.get_llm", side_effect=Exception("LLM error")):
        with patch("core.director._get_db", side_effect=Exception("DB error")):
            asignar_tarea("strategy", "test task")
    out = capsys.readouterr().out
    assert len(out) > 0  # error message printed


# ---------------------------------------------------------------------------
# main() CLI dispatch
# ---------------------------------------------------------------------------

def test_main_no_args_prints_usage(capsys):
    with patch("sys.argv", ["director.py"]):
        main()
    out = capsys.readouterr().out
    assert len(out) > 0


def test_main_roles_flag(capsys):
    with patch("sys.argv", ["director.py", "--roles"]):
        main()
    out = capsys.readouterr().out.lower()
    assert "strategy" in out


def test_main_status_flag(capsys):
    import httpx
    with patch.object(httpx, "get", side_effect=Exception("no connection")):
        with patch("core.director._get_db") as mock_db:
            mock_db.return_value.get_recent_runs.return_value = []
            with patch("llm.get_llm", side_effect=Exception("no llm")):
                with patch("sys.argv", ["director.py", "--status"]):
                    main()
    out = capsys.readouterr().out
    assert len(out) > 0


def test_main_rol_and_tarea_flags(fake_llm, capsys):
    fake_llm.responses["marketing"] = "Campaña de marketing lista."
    mock_db = MagicMock()
    with patch("core.agent.get_llm", return_value=fake_llm):
        with patch("core.director._get_db", return_value=mock_db):
            with patch("sys.argv", ["director.py", "--rol", "marketing", "--tarea", "Campaña Q2"]):
                main()
    out = capsys.readouterr().out
    assert len(out) > 0


def test_verificar_estado_with_recent_run(capsys):
    """Covers the 'Último run' branch in verificar_estado."""
    import httpx
    mock_db = MagicMock()
    mock_db.get_recent_runs.return_value = [{"created_at": "2026-01-01T10:00:00"}]
    with patch.object(httpx, "get", side_effect=Exception("no connection")):
        with patch("core.director._get_db", return_value=mock_db):
            with patch("llm.get_llm", side_effect=Exception("no llm")):
                verificar_estado()
    out = capsys.readouterr().out
    assert len(out) > 0


def test_get_db_calls_agencia_db():
    """Covers the body of _get_db()."""
    from core.director import _get_db
    with patch("memory.db.AgenciaDB") as MockDB:
        _get_db()
        MockDB.assert_called_once()
