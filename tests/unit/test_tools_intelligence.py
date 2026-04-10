"""Tests for tools/intelligence/ and intelligence groups."""
import json
from unittest.mock import patch, MagicMock

import httpx
import pytest

from tools.intelligence.web_search import WebSearchTool
from tools.intelligence.web_scraper import WebScraperTool
from tools.intelligence.competitor_analyzer import CompetitorAnalyzerTool
from tools.intelligence.market_data import MarketDataTool
from tools.intelligence.financial_calculator import FinancialCalculatorTool
from tools.intelligence.banxico import BanxicoTool
from tools.intelligence.quiz_generator import QuizGeneratorTool
from tools.intelligence.learning_tracker import LearningTrackerTool
from tools.intelligence.github_tool import GitHubTool
from tools.intelligence.system_monitor import SystemMonitorTool
from groups.market_intelligence import create_market_intelligence
from groups.financial_advisor import create_financial_advisor
from groups.education_manager import create_education_manager


# ---------------------------------------------------------------------------
# WebSearchTool
# ---------------------------------------------------------------------------

def test_web_search_no_key_uses_duckduckgo():
    ddg_response = {
        "RelatedTopics": [
            {"Text": "Python programming language", "FirstURL": "https://example.com/python"},
            {"Text": "Python tutorial guide", "FirstURL": "https://example.com/tutorial"},
        ]
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = ddg_response
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = WebSearchTool()
        result = tool.run(action="search", query="Python")

    assert result.success
    assert len(result.raw_data["results"]) == 2


def test_web_search_with_serpapi_key():
    serpapi_response = {
        "organic_results": [
            {"title": "Result 1", "link": "https://r1.com", "snippet": "First result"},
        ]
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = serpapi_response
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = WebSearchTool({"serpapi_key": "testkey"})
        result = tool.run(action="search", query="Python")

    assert result.success
    assert result.raw_data["results"][0]["title"] == "Result 1"


def test_web_search_unknown_action_returns_error():
    tool = WebSearchTool()
    result = tool.run(action="invalid")
    assert not result.success
    assert "no soportada" in result.error


def test_web_search_news_no_results():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"RelatedTopics": []}
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = WebSearchTool()
        result = tool.run(action="search_news", query="noticias")

    assert result.success
    assert "Sin noticias" in result.output


# ---------------------------------------------------------------------------
# WebScraperTool
# ---------------------------------------------------------------------------

def test_web_scraper_invalid_url_returns_error():
    tool = WebScraperTool()
    result = tool.run(action="scrape", url="ftp://not-http.com")
    assert not result.success
    assert "http" in result.error.lower()


def test_web_scraper_missing_url_returns_error():
    tool = WebScraperTool()
    result = tool.run(action="scrape", url="")
    assert not result.success


def test_web_scraper_scrapes_content():
    html = "<html><body><main><p>Contenido principal</p></main></body></html>"
    mock_resp = MagicMock()
    mock_resp.text = html
    mock_resp.headers = {"content-type": "text/html", "server": "nginx"}
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = WebScraperTool()
        result = tool.run(action="scrape", url="http://example.com")

    assert result.success
    assert "Contenido principal" in result.output


def test_web_scraper_monitor_price_missing_selector():
    tool = WebScraperTool()
    result = tool.run(action="monitor_price", url="http://example.com")
    assert not result.success
    assert "selector" in result.error.lower()


# ---------------------------------------------------------------------------
# FinancialCalculatorTool
# ---------------------------------------------------------------------------

def test_financial_calculator_roi():
    tool = FinancialCalculatorTool()
    result = tool.run(
        action="calculate_roi",
        investment=100_000.0,
        returns=135_000.0,
        period_years=1.0,
    )
    assert result.success
    assert result.raw_data["roi"] == pytest.approx(35.0)


def test_financial_calculator_roi_zero_investment_returns_error():
    tool = FinancialCalculatorTool()
    result = tool.run(action="calculate_roi", investment=0.0, returns=50_000.0)
    assert not result.success


def test_financial_calculator_break_even():
    tool = FinancialCalculatorTool()
    result = tool.run(
        action="calculate_break_even",
        fixed_costs=50_000.0,
        variable_cost_per_unit=30.0,
        price_per_unit=80.0,
    )
    assert result.success
    assert result.raw_data["units"] == pytest.approx(1000.0)


def test_financial_calculator_price_below_variable_cost():
    tool = FinancialCalculatorTool()
    result = tool.run(
        action="calculate_break_even",
        fixed_costs=10_000.0,
        variable_cost_per_unit=100.0,
        price_per_unit=90.0,
    )
    assert not result.success


def test_financial_calculator_npv():
    tool = FinancialCalculatorTool()
    result = tool.run(
        action="calculate_npv",
        cashflows=[20_000.0, 30_000.0, 40_000.0],
        discount_rate=0.10,
        initial_investment=50_000.0,
    )
    assert result.success
    assert "VPN" in result.output
    assert "npv" in result.raw_data


def test_financial_calculator_npv_no_cashflows_returns_error():
    tool = FinancialCalculatorTool()
    result = tool.run(action="calculate_npv", cashflows=[])
    assert not result.success


def test_financial_calculator_amortization():
    tool = FinancialCalculatorTool()
    result = tool.run(
        action="amortization_table",
        principal=100_000.0,
        annual_rate=0.12,
        periods=24,
    )
    assert result.success
    assert result.raw_data["payment"] > 0


def test_financial_calculator_unknown_action():
    tool = FinancialCalculatorTool()
    result = tool.run(action="unknown")
    assert not result.success


# ---------------------------------------------------------------------------
# BanxicoTool
# ---------------------------------------------------------------------------

def test_banxico_handles_no_token_gracefully():
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = BanxicoTool()
        result = tool.run(action="get_inflation")

    assert result.success
    assert "token" in result.output.lower() or "token" in result.output


def test_banxico_get_exchange_rate_with_token():
    data = {
        "bmx": {
            "series": [{"datos": [{"dato": "17.50", "fecha": "2026-04-01"}]}]
        }
    }
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = data
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = BanxicoTool({"banxico_token": "mytoken"})
        result = tool.run(action="get_exchange_rate")

    assert result.success
    assert "17.50" in result.output


def test_banxico_unknown_action_returns_error():
    tool = BanxicoTool()
    result = tool.run(action="get_something_else")
    assert not result.success


def test_banxico_get_all_consolidates():
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = BanxicoTool()
        result = tool.run(action="get_all")

    assert result.success
    assert "BANXICO" in result.output


# ---------------------------------------------------------------------------
# MarketDataTool
# ---------------------------------------------------------------------------

def test_market_data_get_exchange_rate():
    data = {"rates": {"MXN": 17.5}}
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    mock_resp.raise_for_status = MagicMock()
    mock_resp.status_code = 200

    with patch("httpx.get", return_value=mock_resp):
        tool = MarketDataTool()
        result = tool.run(action="get_exchange_rate", from_currency="USD", to_currency="MXN")

    assert result.success
    assert "17.5" in result.output or "17.50" in result.output


def test_market_data_unknown_action_returns_error():
    tool = MarketDataTool()
    result = tool.run(action="unknown_action")
    assert not result.success


# ---------------------------------------------------------------------------
# QuizGeneratorTool
# ---------------------------------------------------------------------------

def test_quiz_generator_generates_structure(tmp_path):
    with patch("tools.intelligence.quiz_generator._DATA_DIR", tmp_path):
        tool = QuizGeneratorTool()
        result = tool.run(
            action="generate_quiz",
            topic="Inteligencia Artificial",
            num_questions=3,
            difficulty="medium",
        )
    assert result.success
    assert result.raw_data["num_questions"] == 3
    assert result.raw_data["topic"] == "Inteligencia Artificial"
    assert len(result.raw_data["questions"]) == 3


def test_quiz_generator_missing_topic_returns_error():
    tool = QuizGeneratorTool()
    result = tool.run(action="generate_quiz", topic="")
    assert not result.success
    assert "topic" in result.error.lower()


def test_quiz_generator_grade_responses(tmp_path):
    with patch("tools.intelligence.quiz_generator._DATA_DIR", tmp_path):
        tool = QuizGeneratorTool()
        gen = tool.run(
            action="generate_quiz",
            topic="Python",
            num_questions=2,
            difficulty="easy",
        )
    quiz_id = gen.raw_data["id"]
    questions = gen.raw_data["questions"]

    with patch("tools.intelligence.quiz_generator._DATA_DIR", tmp_path):
        responses = {f"q{i}": q["answer"] for i, q in enumerate(questions)}
        result = tool.run(action="grade_responses", quiz_id=quiz_id, responses=responses)

    assert result.success
    assert result.raw_data["score"] == pytest.approx(100.0)
    assert result.raw_data["passed"] is True


def test_quiz_generator_grade_missing_quiz_returns_error(tmp_path):
    with patch("tools.intelligence.quiz_generator._DATA_DIR", tmp_path):
        tool = QuizGeneratorTool()
        result = tool.run(action="grade_responses", quiz_id="NOTEXIST")
    assert not result.success


def test_quiz_generator_unknown_action_returns_error():
    tool = QuizGeneratorTool()
    result = tool.run(action="unknown")
    assert not result.success


# ---------------------------------------------------------------------------
# LearningTrackerTool
# ---------------------------------------------------------------------------

def test_learning_tracker_record_and_report(tmp_path):
    data_file = tmp_path / "learning_progress.json"
    with patch("tools.intelligence.learning_tracker._DATA_FILE", data_file):
        tool = LearningTrackerTool()
        tool.run(action="record_progress", student_id="S001",
                 module="Python Básico", score=85.0, time_spent_min=60)
        tool.run(action="record_progress", student_id="S001",
                 module="Python Avanzado", score=90.0, time_spent_min=90)
        result = tool.run(action="get_report", student_id="S001")

    assert result.success
    assert result.raw_data["avg"] == pytest.approx(87.5)
    assert result.raw_data["total_time_min"] == 150


def test_learning_tracker_identify_weak_areas(tmp_path):
    data_file = tmp_path / "learning_progress.json"
    with patch("tools.intelligence.learning_tracker._DATA_FILE", data_file):
        tool = LearningTrackerTool()
        tool.run(action="record_progress", student_id="S002",
                 module="Algebra", score=60.0, time_spent_min=45)
        tool.run(action="record_progress", student_id="S002",
                 module="Cálculo", score=55.0, time_spent_min=30)
        result = tool.run(action="identify_weak", student_id="S002", threshold=70.0)

    assert result.success
    assert "Algebra" in result.output or "Cálculo" in result.output
    assert len(result.raw_data["weak_modules"]) == 2


def test_learning_tracker_report_no_records_returns_error(tmp_path):
    data_file = tmp_path / "learning_progress.json"
    with patch("tools.intelligence.learning_tracker._DATA_FILE", data_file):
        tool = LearningTrackerTool()
        result = tool.run(action="get_report", student_id="GHOST")
    assert not result.success


def test_learning_tracker_list_students(tmp_path):
    data_file = tmp_path / "learning_progress.json"
    with patch("tools.intelligence.learning_tracker._DATA_FILE", data_file):
        tool = LearningTrackerTool()
        tool.run(action="record_progress", student_id="A1", module="M1", score=75.0)
        tool.run(action="record_progress", student_id="A2", module="M1", score=80.0)
        result = tool.run(action="list_students")
    assert result.success
    assert "A1" in result.output
    assert "A2" in result.output


# ---------------------------------------------------------------------------
# GitHubTool
# ---------------------------------------------------------------------------

def test_github_tool_no_token_returns_error():
    tool = GitHubTool()
    result = tool.run(action="create_issue", repo="owner/repo", title="Bug")
    assert not result.success
    assert "github_token" in result.error


def test_github_tool_get_issues_success():
    issues_data = [
        {"number": 1, "title": "Bug crítico", "state": "open"},
        {"number": 2, "title": "Feature request", "state": "open"},
    ]
    mock_resp = MagicMock()
    mock_resp.json.return_value = issues_data
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = GitHubTool({"github_token": "ghp_test"})
        result = tool.run(action="get_issues", repo="owner/repo")

    assert result.success
    assert "#1" in result.output


def test_github_tool_create_issue_success():
    issue_data = {"number": 42, "html_url": "https://github.com/owner/repo/issues/42"}
    mock_resp = MagicMock()
    mock_resp.json.return_value = issue_data
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.post", return_value=mock_resp):
        tool = GitHubTool({"github_token": "ghp_test"})
        result = tool.run(
            action="create_issue",
            repo="owner/repo",
            title="Test Issue",
            body="Description",
        )

    assert result.success
    assert "#42" in result.output


def test_github_tool_unknown_action_returns_error():
    tool = GitHubTool({"github_token": "ghp_test"})
    result = tool.run(action="delete_repo")
    assert not result.success


# ---------------------------------------------------------------------------
# SystemMonitorTool
# ---------------------------------------------------------------------------

def test_system_monitor_cpu():
    mock_psutil = MagicMock()
    mock_psutil.cpu_percent.return_value = 42.5
    mock_psutil.cpu_count.return_value = 8
    mock_psutil.cpu_freq.return_value = MagicMock(current=3200)

    with patch.object(SystemMonitorTool, "_check_psutil", return_value=mock_psutil):
        tool = SystemMonitorTool()
        result = tool.run(action="get_cpu")

    assert result.success
    assert result.raw_data["cpu_percent"] == 42.5
    assert result.raw_data["cpu_count"] == 8


def test_system_monitor_memory():
    mock_mem = MagicMock()
    mock_mem.percent = 65.0
    mock_mem.used = 8_000_000_000
    mock_mem.available = 4_000_000_000
    mock_mem.total = 16_000_000_000

    mock_psutil = MagicMock()
    mock_psutil.virtual_memory.return_value = mock_mem

    with patch.object(SystemMonitorTool, "_check_psutil", return_value=mock_psutil):
        tool = SystemMonitorTool()
        result = tool.run(action="get_memory")

    assert result.success
    assert result.raw_data["percent"] == 65.0


def test_system_monitor_get_all():
    mock_mem = MagicMock(
        percent=50.0, used=8e9, available=8e9, total=16e9
    )
    mock_disk = MagicMock(percent=30.0, used=100e9, free=200e9, total=300e9)
    mock_psutil = MagicMock()
    mock_psutil.cpu_percent.return_value = 20.0
    mock_psutil.cpu_count.return_value = 4
    mock_psutil.cpu_freq.return_value = None
    mock_psutil.virtual_memory.return_value = mock_mem
    mock_psutil.disk_usage.return_value = mock_disk

    with patch.object(SystemMonitorTool, "_check_psutil", return_value=mock_psutil):
        tool = SystemMonitorTool()
        result = tool.run(action="get_all")

    assert result.success
    assert "cpu" in result.raw_data["sections"]
    assert "memory" in result.raw_data["sections"]


def test_system_monitor_no_psutil_returns_error():
    with patch.object(SystemMonitorTool, "_check_psutil", return_value=None):
        tool = SystemMonitorTool()
        result = tool.run(action="get_cpu")
    assert not result.success
    assert "psutil" in result.error


def test_system_monitor_check_service_found():
    mock_proc = MagicMock()
    mock_proc.info = {"name": "python.exe", "pid": 1234}

    mock_psutil = MagicMock()
    mock_psutil.process_iter.return_value = [mock_proc]

    with patch.object(SystemMonitorTool, "_check_psutil", return_value=mock_psutil):
        tool = SystemMonitorTool()
        result = tool.run(action="check_service", service_name="python")

    assert result.success
    assert "ACTIVO" in result.output
    assert result.raw_data["found"] is True


# ---------------------------------------------------------------------------
# Group creation tests
# ---------------------------------------------------------------------------

def test_create_market_intelligence_group():
    group = create_market_intelligence()
    assert group.name == "market_intelligence"
    agent_roles = [a.role for a in group.agents]
    assert "data_collector" in agent_roles
    assert "competitor_analyzer" in agent_roles
    assert "trend_identifier" in agent_roles
    assert "strategic_reporter" in agent_roles


def test_create_financial_advisor_group():
    group = create_financial_advisor()
    assert group.name == "financial_advisor"
    agent_roles = [a.role for a in group.agents]
    assert "data_gatherer" in agent_roles
    assert "financial_analyst" in agent_roles
    assert "risk_evaluator" in agent_roles
    assert "recommendation_writer" in agent_roles


def test_create_education_manager_group():
    group = create_education_manager()
    assert group.name == "education_manager"
    agent_roles = [a.role for a in group.agents]
    assert "curriculum_designer" in agent_roles
    assert "content_creator" in agent_roles
    assert "assessment_builder" in agent_roles
    assert "progress_tracker" in agent_roles


# ---------------------------------------------------------------------------
# CompetitorAnalyzerTool
# ---------------------------------------------------------------------------

def _make_competitor_html():
    return """<html>
<head>
  <title>Empresa Rival S.A.</title>
  <meta name="description" content="Líder en soluciones digitales">
  <script src="/wp-content/themes/main.js"></script>
  <script src="https://cdn.example.com/jquery.min.js"></script>
</head>
<body>
  <h1>Bienvenidos</h1>
  <h2>Nuestros servicios</h2>
  <h2>Contáctanos</h2>
  <a href="/pagina-interna">Interna</a>
  <a href="https://externo.com">Externa</a>
</body>
</html>"""


def test_competitor_analyzer_invalid_url():
    tool = CompetitorAnalyzerTool()
    result = tool.run(action="analyze_website", url="ftp://invalid.com")
    assert not result.success


def test_competitor_analyzer_analyze_website():
    mock_resp = MagicMock()
    mock_resp.text = _make_competitor_html()
    mock_resp.headers = {"server": "nginx/1.18"}
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = CompetitorAnalyzerTool()
        result = tool.run(action="analyze_website", url="http://rival.com")

    assert result.success
    assert result.raw_data["title"] == "Empresa Rival S.A."
    assert "WordPress" in result.raw_data["technologies"] or "jQuery" in result.raw_data["technologies"]
    assert result.raw_data["word_count"] > 0


def test_competitor_analyzer_detects_technologies():
    html = """<html><head><title>Test</title>
    <script src="https://cdn.shopify.com/shopify.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/17.0/react.min.js"></script>
    </head><body>Content</body></html>"""
    mock_resp = MagicMock()
    mock_resp.text = html
    mock_resp.headers = {"server": "cloudflare"}
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = CompetitorAnalyzerTool()
        result = tool.run(action="analyze_website", url="http://shop.com")

    assert result.success
    techs = result.raw_data["technologies"]
    assert "Shopify" in techs or "React" in techs


def test_competitor_analyzer_compare_social():
    mock_resp = MagicMock()
    mock_resp.text = "<html><head><title>Competitor Page</title></head><body>Text</body></html>"
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = CompetitorAnalyzerTool()
        result = tool.run(
            action="compare_social",
            accounts=["http://instagram.com/rival1", "http://facebook.com/rival2"],
        )

    assert result.success
    assert len(result.raw_data["accounts"]) == 2


def test_competitor_analyzer_compare_social_no_accounts():
    tool = CompetitorAnalyzerTool()
    result = tool.run(action="compare_social", accounts=[])
    assert not result.success


def test_competitor_analyzer_compare_social_invalid_url():
    tool = CompetitorAnalyzerTool()
    result = tool.run(action="compare_social", accounts=["not-a-url"])
    assert result.success
    assert result.raw_data["accounts"][0]["error"] == "URL inválida"


def test_competitor_analyzer_unknown_action():
    tool = CompetitorAnalyzerTool()
    result = tool.run(action="scrape_everything")
    assert not result.success


# ---------------------------------------------------------------------------
# WebScraperTool — additional coverage
# ---------------------------------------------------------------------------

def test_web_scraper_extract_text():
    html = """<html><body>
    <article><p>Este es un párrafo con suficiente contenido para ser extraído correctamente.</p>
    <p>Otro párrafo con información relevante para el análisis del sitio web.</p></article>
    </body></html>"""
    mock_resp = MagicMock()
    mock_resp.text = html
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = WebScraperTool()
        result = tool.run(action="extract_text", url="http://example.com/article")

    assert result.success


def test_web_scraper_extract_text_invalid_url():
    tool = WebScraperTool()
    result = tool.run(action="extract_text", url="not-http")
    assert not result.success


def test_web_scraper_scrape_with_selectors():
    html = """<html><body>
    <span class="price">$1,299.00</span>
    <h1 class="title">Producto Premium</h1>
    </body></html>"""
    mock_resp = MagicMock()
    mock_resp.text = html
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = WebScraperTool()
        result = tool.run(
            action="scrape",
            url="http://shop.com/producto",
            selectors={"price": ".price", "title": ".title"},
        )

    assert result.success
    assert result.raw_data["price"] == "$1,299.00"
    assert result.raw_data["title"] == "Producto Premium"


def test_web_scraper_monitor_price_found():
    html = "<html><body><span class='price'>$599.00</span></body></html>"
    mock_resp = MagicMock()
    mock_resp.text = html
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = WebScraperTool()
        result = tool.run(
            action="monitor_price",
            url="http://store.com",
            selector=".price",
        )

    assert result.success
    assert "$599.00" in result.output
    assert result.raw_data["value"] == "$599.00"


def test_web_scraper_scrape_removes_noise_tags():
    html = """<html><body>
    <nav>Navegación que debe eliminarse</nav>
    <script>alert('js noise')</script>
    <p>Contenido real del artículo</p>
    <footer>Footer a eliminar</footer>
    </body></html>"""
    mock_resp = MagicMock()
    mock_resp.text = html
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = WebScraperTool()
        result = tool.run(action="scrape", url="http://example.com")

    assert result.success
    assert "Contenido real del artículo" in result.output
    assert "alert" not in result.output


# ---------------------------------------------------------------------------
# MarketDataTool — additional coverage
# ---------------------------------------------------------------------------

def test_market_data_get_stock():
    data = {
        "chart": {
            "result": [{
                "meta": {
                    "regularMarketPrice": 185.5,
                    "previousClose": 180.0,
                    "regularMarketVolume": 5_000_000,
                    "fiftyTwoWeekLow": 150.0,
                    "fiftyTwoWeekHigh": 200.0,
                    "currency": "USD",
                }
            }]
        }
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = MarketDataTool()
        result = tool.run(action="get_stock", ticker="AAPL")

    assert result.success
    assert result.raw_data["ticker"] == "AAPL"
    assert result.raw_data["price"] == 185.5


def test_market_data_get_crypto():
    data = {
        "bitcoin": {
            "usd": 65_000.0,
            "mxn": 1_100_000.0,
            "usd_24h_change": 2.5,
        }
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = data
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = MarketDataTool()
        result = tool.run(action="get_crypto", symbol="bitcoin")

    assert result.success
    assert result.raw_data["usd"] == 65_000.0


def test_market_data_get_crypto_not_found():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {}
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = MarketDataTool()
        result = tool.run(action="get_crypto", symbol="fakecoin")

    assert not result.success


def test_market_data_get_indicators_mx():
    """MX indicators delegate to BanxicoTool."""
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = MarketDataTool()
        result = tool.run(action="get_indicators", country="MX")

    assert result.success  # BanxicoTool handles 401 gracefully


# ---------------------------------------------------------------------------
# ImageResizeTool
# ---------------------------------------------------------------------------

def test_image_resize_missing_input_path():
    from tools.media.image_resize import ImageResizeTool
    tool = ImageResizeTool()
    result = tool.run(action="resize", input_path="")
    assert not result.success
    assert "input_path" in result.error


def test_image_resize_file_not_found():
    from tools.media.image_resize import ImageResizeTool
    tool = ImageResizeTool()
    result = tool.run(action="resize", input_path="/nonexistent/image.png")
    assert not result.success
    assert "no encontrado" in result.error


def test_image_resize_success(tmp_path):
    from tools.media.image_resize import ImageResizeTool
    img_path = tmp_path / "test.png"
    img_path.write_bytes(b"fake")

    mock_img = MagicMock()
    mock_pil = MagicMock()
    mock_pil.Image.open.return_value = mock_img
    mock_img.resize.return_value = mock_img

    import sys
    sys.modules["PIL"] = mock_pil
    sys.modules["PIL.Image"] = mock_pil.Image

    with patch.dict("sys.modules", {"PIL": mock_pil, "PIL.Image": mock_pil.Image}):
        mock_pil.Image.LANCZOS = 1
        mock_pil.Image.open.return_value = mock_img
        mock_img.resize.return_value = mock_img
        tool = ImageResizeTool()
        result = tool.run(
            action="resize",
            input_path=str(img_path),
            width=800,
            height=600,
            output_path=str(tmp_path / "out.png"),
        )

    assert result.success
    assert result.raw_data["width"] == 800


def test_image_convert_missing_input():
    from tools.media.image_resize import ImageResizeTool
    tool = ImageResizeTool()
    result = tool.run(action="convert", input_path="")
    assert not result.success


def test_image_convert_file_not_found():
    from tools.media.image_resize import ImageResizeTool
    tool = ImageResizeTool()
    result = tool.run(action="convert", input_path="/no/such/file.png")
    assert not result.success


def test_image_resize_unknown_action():
    from tools.media.image_resize import ImageResizeTool
    tool = ImageResizeTool()
    result = tool.run(action="crop")
    assert not result.success


# ---------------------------------------------------------------------------
# GitHubTool — additional coverage
# ---------------------------------------------------------------------------

def test_github_get_repo_info():
    repo_data = {
        "full_name": "owner/repo",
        "description": "Test repo",
        "stargazers_count": 42,
        "forks_count": 5,
        "language": "Python",
        "open_issues_count": 3,
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = repo_data
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = GitHubTool({"github_token": "ghp_test"})
        result = tool.run(action="get_repo_info", repo="owner/repo")

    assert result.success
    assert "owner/repo" in result.output
    assert "42" in result.output


def test_github_get_repo_info_no_token():
    tool = GitHubTool()
    result = tool.run(action="get_repo_info", repo="owner/repo")
    assert not result.success


def test_github_create_pr_summary():
    pr_data = {
        "title": "Fix critical bug",
        "state": "closed",
        "merged": True,
        "additions": 50,
        "deletions": 10,
        "changed_files": 3,
        "user": {"login": "developer"},
    }
    mock_resp = MagicMock()
    mock_resp.json.return_value = pr_data
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.get", return_value=mock_resp):
        tool = GitHubTool({"github_token": "ghp_test"})
        result = tool.run(action="create_pr_summary", repo="owner/repo", pr_number=7)

    assert result.success
    assert "Fix critical bug" in result.output
    assert "developer" in result.output
