"""Tests for tools/web/: WordPress, Webflow, Ghost."""
from unittest.mock import MagicMock, patch

import pytest
import httpx  # ensure module is loaded so patching works

from tools.web.wordpress import WordPressTool
from tools.web.webflow import WebflowTool
from tools.web.ghost import GhostTool
from tools.base import ToolRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _creds_wp():
    return {
        "url": "https://myblog.com",
        "username": "admin",
        "app_password": "abcd 1234 efgh",
    }


def _creds_wf():
    return {"api_token": "wf-token-123", "site_id": "site-abc"}


def _creds_ghost():
    return {
        "url": "https://myblog.ghost.io",
        "admin_api_key": "aabbcc:deadbeefdeadbeef",
    }


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def test_web_tools_registered():
    names = [t["name"] for t in ToolRegistry.list_all()]
    for name in ("wordpress", "webflow", "ghost"):
        assert name in names


# ---------------------------------------------------------------------------
# WordPress — missing credentials
# ---------------------------------------------------------------------------

def test_wordpress_no_url_returns_error():
    t = WordPressTool(credentials={"username": "u", "app_password": "p"})
    r = t.run(action="create_post", title="Test", content="body")
    assert r.success is False
    assert "Credenciales WordPress" in r.error


def test_wordpress_no_username_returns_error():
    t = WordPressTool(credentials={"url": "https://blog.com", "app_password": "p"})
    r = t.run(action="create_post", title="Test", content="body")
    assert r.success is False
    assert "Credenciales WordPress" in r.error


def test_wordpress_no_app_password_returns_error():
    t = WordPressTool(credentials={"url": "https://blog.com", "username": "u"})
    r = t.run(action="get_posts")
    assert r.success is False
    assert "Credenciales WordPress" in r.error


def test_wordpress_upload_nonexistent_file_returns_error():
    t = WordPressTool(credentials=_creds_wp())
    r = t.run(action="upload_media", file_path="/nonexistent/image.jpg")
    assert r.success is False
    assert "no encontrado" in r.error


def test_wordpress_update_post_nothing_to_update():
    t = WordPressTool(credentials=_creds_wp())
    r = t._update_post(post_id=1)
    assert r.success is False
    assert "Nada que actualizar" in r.error


def test_wordpress_unsupported_action():
    t = WordPressTool(credentials=_creds_wp())
    r = t.run(action="delete_post")
    assert r.success is False
    assert "no soportada" in r.error


# ---------------------------------------------------------------------------
# WordPress — success with mocked httpx
# ---------------------------------------------------------------------------

def test_wordpress_create_post_success():
    t = WordPressTool(credentials=_creds_wp())
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"id": 42, "link": "https://myblog.com/?p=42"}
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.post", return_value=mock_resp):
        r = t._create_post(title="Hello", content="<p>World</p>", status="publish")

    assert r.success is True
    assert "42" in r.output
    assert r.raw_data["post_id"] == 42


def test_wordpress_get_posts_success():
    t = WordPressTool(credentials=_creds_wp())
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"id": 1, "title": {"rendered": "Post One"}, "status": "publish"},
        {"id": 2, "title": {"rendered": "Post Two"}, "status": "draft"},
    ]
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_resp):
        r = t._get_posts()

    assert r.success is True
    assert "Post One" in r.output
    assert len(r.raw_data["posts"]) == 2


def test_wordpress_get_posts_empty():
    t = WordPressTool(credentials=_creds_wp())
    mock_resp = MagicMock()
    mock_resp.json.return_value = []
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_resp):
        r = t._get_posts()

    assert r.success is True
    assert "Sin posts" in r.output


def test_wordpress_update_post_success():
    t = WordPressTool(credentials=_creds_wp())
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.patch", return_value=mock_resp):
        r = t._update_post(post_id=5, title="New Title")

    assert r.success is True
    assert "5" in r.output


def test_wordpress_get_categories_success():
    t = WordPressTool(credentials=_creds_wp())
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"id": 1, "name": "Tech"},
        {"id": 2, "name": "Marketing"},
    ]
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_resp):
        r = t._get_categories()

    assert r.success is True
    assert "Tech" in r.output
    assert "Marketing" in r.output


def test_wordpress_http_error_returns_error():
    t = WordPressTool(credentials=_creds_wp())
    with patch("httpx.post", side_effect=Exception("connection refused")):
        r = t._create_post(title="X", content="Y")
    assert r.success is False
    assert "connection refused" in r.error


# ---------------------------------------------------------------------------
# Webflow — missing credentials
# ---------------------------------------------------------------------------

def test_webflow_no_api_token_returns_error():
    t = WebflowTool(credentials={"site_id": "abc"})
    r = t.run(action="create_item", collection_id="col1", fields={"name": "Test"})
    assert r.success is False
    assert "api_token" in r.error


def test_webflow_publish_no_site_id_returns_error():
    t = WebflowTool(credentials={"api_token": "tok"})
    r = t.run(action="publish_site")
    assert r.success is False
    assert "site_id" in r.error


def test_webflow_unsupported_action():
    t = WebflowTool(credentials=_creds_wf())
    r = t.run(action="delete_item")
    assert r.success is False
    assert "no soportada" in r.error


# ---------------------------------------------------------------------------
# Webflow — success with mocked httpx
# ---------------------------------------------------------------------------

def test_webflow_create_item_success():
    t = WebflowTool(credentials=_creds_wf())
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"id": "item-999"}
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.post", return_value=mock_resp):
        r = t._create_item(collection_id="col1", fields={"name": "Blog Post"})

    assert r.success is True
    assert "item-999" in r.output
    assert r.raw_data["item_id"] == "item-999"


def test_webflow_update_item_success():
    t = WebflowTool(credentials=_creds_wf())
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.patch", return_value=mock_resp):
        r = t._update_item(collection_id="col1", item_id="item-999", fields={"name": "Updated"})

    assert r.success is True
    assert "item-999" in r.output


def test_webflow_list_items_success():
    t = WebflowTool(credentials=_creds_wf())
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "items": [
            {"id": "i1", "fieldData": {"name": "Post A"}},
            {"id": "i2", "fieldData": {"name": "Post B"}},
        ]
    }
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_resp):
        r = t._list_items(collection_id="col1")

    assert r.success is True
    assert "Post A" in r.output
    assert len(r.raw_data["items"]) == 2


def test_webflow_list_items_empty():
    t = WebflowTool(credentials=_creds_wf())
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"items": []}
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_resp):
        r = t._list_items(collection_id="col1")

    assert r.success is True
    assert "Sin items" in r.output


def test_webflow_publish_site_success():
    t = WebflowTool(credentials=_creds_wf())
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.post", return_value=mock_resp):
        r = t._publish_site()

    assert r.success is True
    assert "publicado" in r.output


def test_webflow_http_error_returns_error():
    t = WebflowTool(credentials=_creds_wf())
    with patch("httpx.post", side_effect=Exception("timeout")):
        r = t._create_item(collection_id="col1", fields={})
    assert r.success is False
    assert "timeout" in r.error


# ---------------------------------------------------------------------------
# Ghost — missing credentials
# ---------------------------------------------------------------------------

def test_ghost_no_url_returns_error():
    t = GhostTool(credentials={"admin_api_key": "aabb:ccdd"})
    r = t.run(action="create_post", title="T", html="<p>H</p>")
    assert r.success is False
    assert "url" in r.error


def test_ghost_no_admin_api_key_returns_error():
    t = GhostTool(credentials={"url": "https://blog.ghost.io"})
    r = t.run(action="create_post", title="T", html="<p>H</p>")
    assert r.success is False


def test_ghost_invalid_api_key_format_returns_error():
    # key without ":" is invalid
    t = GhostTool(credentials={"url": "https://blog.ghost.io", "admin_api_key": "nodivider"})
    r = t.run(action="create_post", title="T", html="<p>H</p>")
    assert r.success is False
    assert "inválida" in r.error


def test_ghost_update_post_nothing_to_update():
    t = GhostTool(credentials=_creds_ghost())
    # Even with valid creds structure, if jwt fails, error is returned
    # Test the body-empty guard: patch jwt to return a token
    with patch.object(t, "_get_jwt", return_value="fake-token"):
        r = t._update_post(post_id="p1")
    assert r.success is False
    assert "Nada que actualizar" in r.error


def test_ghost_unsupported_action():
    t = GhostTool(credentials=_creds_ghost())
    r = t.run(action="delete_post")
    assert r.success is False
    assert "no soportada" in r.error


# ---------------------------------------------------------------------------
# Ghost — success with mocked jwt + httpx
# ---------------------------------------------------------------------------

def test_ghost_create_post_success():
    t = GhostTool(credentials=_creds_ghost())
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "posts": [{"id": "ghost-post-1", "url": "https://blog.ghost.io/p/hello"}]
    }
    mock_resp.raise_for_status.return_value = None

    with patch.object(t, "_get_jwt", return_value="fake-jwt-token"):
        with patch("httpx.post", return_value=mock_resp):
            r = t._create_post(title="Hello Ghost", html="<p>Content</p>")

    assert r.success is True
    assert "Hello Ghost" in r.output
    assert r.raw_data["post_id"] == "ghost-post-1"


def test_ghost_get_posts_success():
    t = GhostTool(credentials=_creds_ghost())
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "posts": [
            {"id": "p1", "title": "First Post", "status": "published"},
            {"id": "p2", "title": "Second Post", "status": "published"},
        ]
    }
    mock_resp.raise_for_status.return_value = None

    with patch.object(t, "_get_jwt", return_value="fake-token"):
        with patch("httpx.get", return_value=mock_resp):
            r = t._get_posts()

    assert r.success is True
    assert "First Post" in r.output
    assert len(r.raw_data["posts"]) == 2


def test_ghost_get_posts_empty():
    t = GhostTool(credentials=_creds_ghost())
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"posts": []}
    mock_resp.raise_for_status.return_value = None

    with patch.object(t, "_get_jwt", return_value="fake-token"):
        with patch("httpx.get", return_value=mock_resp):
            r = t._get_posts()

    assert r.success is True
    assert "Sin posts" in r.output


def test_ghost_update_post_success():
    t = GhostTool(credentials=_creds_ghost())
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None

    with patch.object(t, "_get_jwt", return_value="fake-token"):
        with patch("httpx.put", return_value=mock_resp):
            r = t._update_post(post_id="p1", status="published")

    assert r.success is True
    assert "p1" in r.output


def test_ghost_http_error_returns_error():
    t = GhostTool(credentials=_creds_ghost())
    with patch.object(t, "_get_jwt", return_value="fake-token"):
        with patch("httpx.post", side_effect=Exception("network error")):
            r = t._create_post(title="T", html="<p>X</p>")
    assert r.success is False
    assert "network error" in r.error
