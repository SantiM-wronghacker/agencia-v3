"""Tests for groups/ — factory functions and agent composition."""
from unittest.mock import MagicMock, patch

import pytest

from memory.db import AgenciaDB


def _fake_llm():
    llm = MagicMock()
    llm.provider_name = "fake"
    llm.generate.return_value = "ok"
    return llm


# ---------------------------------------------------------------------------
# Agent count and roles
# ---------------------------------------------------------------------------

def test_content_pipeline_has_four_agents():
    with patch("core.agent.get_llm", return_value=_fake_llm()):
        from groups.content_pipeline import create_content_pipeline
        group = create_content_pipeline()
    assert len(group.agents) == 4
    assert group.agents[0].role == "researcher"
    assert group.agents[-1].role == "reviewer"


def test_business_analysis_has_four_agents():
    with patch("core.agent.get_llm", return_value=_fake_llm()):
        from groups.business_analysis import create_business_analysis
        assert len(create_business_analysis().agents) == 4


def test_legal_review_has_four_agents():
    with patch("core.agent.get_llm", return_value=_fake_llm()):
        from groups.legal_review import create_legal_review
        assert len(create_legal_review().agents) == 4


def test_ops_automation_has_three_agents():
    with patch("core.agent.get_llm", return_value=_fake_llm()):
        from groups.ops_automation import create_ops_automation
        assert len(create_ops_automation().agents) == 3


# ---------------------------------------------------------------------------
# Mode
# ---------------------------------------------------------------------------

def test_all_groups_are_pipeline_mode():
    with patch("core.agent.get_llm", return_value=_fake_llm()):
        from groups.content_pipeline import create_content_pipeline
        from groups.business_analysis import create_business_analysis
        from groups.legal_review import create_legal_review
        from groups.ops_automation import create_ops_automation
        factories = [
            create_content_pipeline,
            create_business_analysis,
            create_legal_review,
            create_ops_automation,
        ]
    for factory in factories:
        with patch("core.agent.get_llm", return_value=_fake_llm()):
            assert factory().mode == "pipeline", f"{factory.__name__} no es pipeline"


# ---------------------------------------------------------------------------
# DB propagation
# ---------------------------------------------------------------------------

def test_groups_accept_db_parameter():
    db = AgenciaDB(":memory:")
    with patch("core.agent.get_llm", return_value=_fake_llm()):
        from groups.content_pipeline import create_content_pipeline
        group = create_content_pipeline(db=db)
    assert group.db is db


def test_group_name_matches_function():
    with patch("core.agent.get_llm", return_value=_fake_llm()):
        from groups.content_pipeline import create_content_pipeline
        from groups.business_analysis import create_business_analysis
        from groups.legal_review import create_legal_review
        from groups.ops_automation import create_ops_automation
        assert create_content_pipeline().name == "content_pipeline"
        assert create_business_analysis().name == "business_analysis"
        assert create_legal_review().name == "legal_review"
        assert create_ops_automation().name == "ops_automation"
