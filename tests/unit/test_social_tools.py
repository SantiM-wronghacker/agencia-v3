"""Tests for tools/social/ and tools/email/smtp.py."""
from unittest.mock import MagicMock, patch

import pytest

from tools.social.instagram import InstagramTool
from tools.social.facebook import FacebookTool
from tools.social.linkedin import LinkedInTool
from tools.social.tiktok import TikTokTool
from tools.social.twitter import TwitterTool
from tools.email.smtp import SMTPTool
from tools.base import ToolRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _creds_instagram():
    return {"access_token": "tok", "account_id": "123"}

def _creds_facebook():
    return {"page_token": "ptok", "page_id": "456"}

def _creds_linkedin():
    return {"access_token": "ltok", "org_id": "789"}

def _creds_tiktok():
    return {"access_token": "ttok", "open_id": "oid"}

def _creds_twitter():
    return {"bearer_token": "btok"}

def _creds_smtp():
    return {
        "smtp_host": "smtp.example.com",
        "smtp_port": "587",
        "smtp_user": "user@example.com",
        "smtp_password": "secret",
    }


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def test_all_social_tools_registered():
    names = [t["name"] for t in ToolRegistry.list_all()]
    for name in ("instagram", "facebook", "linkedin", "tiktok", "twitter", "smtp_email"):
        assert name in names


# ---------------------------------------------------------------------------
# Missing credentials — all tools must return error without HTTP calls
# ---------------------------------------------------------------------------

def test_instagram_no_access_token_returns_error():
    t = InstagramTool(credentials={"account_id": "123"})
    r = t.run(action="post_image", caption="test")
    assert r.success is False
    assert "access_token" in r.error

def test_instagram_no_account_id_returns_error():
    t = InstagramTool(credentials={"access_token": "tok"})
    r = t.run(action="post_image", caption="test")
    assert r.success is False
    assert "account_id" in r.error

def test_facebook_no_page_token_returns_error():
    t = FacebookTool(credentials={"page_id": "1"})
    r = t.run(action="post_text", message="hello")
    assert r.success is False
    assert "page_token" in r.error

def test_facebook_no_page_id_returns_error():
    t = FacebookTool(credentials={"page_token": "t"})
    r = t.run(action="post_text", message="hello")
    assert r.success is False
    assert "page_id" in r.error

def test_linkedin_no_access_token_returns_error():
    t = LinkedInTool(credentials={})
    r = t.run(action="post_text", text="hello")
    assert r.success is False
    assert "access_token" in r.error

def test_tiktok_no_access_token_returns_error():
    t = TikTokTool(credentials={"open_id": "oid"})
    r = t.run(action="upload_video", video_path="/fake/path.mp4", caption="test")
    assert r.success is False
    assert "access_token" in r.error

def test_tiktok_no_open_id_returns_error():
    t = TikTokTool(credentials={"access_token": "tok"})
    r = t.run(action="upload_video", video_path="/fake/path.mp4", caption="test")
    assert r.success is False
    assert "open_id" in r.error

def test_twitter_no_bearer_token_returns_error():
    t = TwitterTool(credentials={})
    r = t.run(action="post_tweet", text="hello")
    assert r.success is False
    assert "bearer_token" in r.error

def test_smtp_missing_host_returns_error():
    t = SMTPTool(credentials={"smtp_port": "587", "smtp_user": "u", "smtp_password": "p"})
    r = t.run(action="send", to="a@b.com", subject="S", body="B")
    assert r.success is False
    assert "smtp_host" in r.error

def test_smtp_missing_password_returns_error():
    t = SMTPTool(credentials={"smtp_host": "h", "smtp_port": "587", "smtp_user": "u"})
    r = t.run(action="send", to="a@b.com", subject="S", body="B")
    assert r.success is False
    assert "smtp_password" in r.error


# ---------------------------------------------------------------------------
# Unsupported actions
# ---------------------------------------------------------------------------

def test_instagram_unsupported_action():
    t = InstagramTool(credentials=_creds_instagram())
    r = t.run(action="delete_post")
    assert r.success is False
    assert "no soportada" in r.error

def test_facebook_unsupported_action():
    t = FacebookTool(credentials=_creds_facebook())
    r = t.run(action="delete_post")
    assert r.success is False
    assert "no soportada" in r.error

def test_linkedin_unsupported_action():
    t = LinkedInTool(credentials=_creds_linkedin())
    r = t.run(action="delete_post")
    assert r.success is False
    assert "no soportada" in r.error

def test_tiktok_unsupported_action():
    t = TikTokTool(credentials=_creds_tiktok())
    r = t.run(action="delete_video")
    assert r.success is False
    assert "no soportada" in r.error

def test_twitter_unsupported_action():
    t = TwitterTool(credentials=_creds_twitter())
    r = t.run(action="delete_tweet")
    assert r.success is False
    assert "no soportada" in r.error

def test_smtp_unsupported_action():
    t = SMTPTool(credentials=_creds_smtp())
    r = t.run(action="delete_email")
    assert r.success is False
    assert "no soportada" in r.error


# ---------------------------------------------------------------------------
# Twitter — tweet length validation
# ---------------------------------------------------------------------------

def test_twitter_tweet_too_long_returns_error():
    t = TwitterTool(credentials=_creds_twitter())
    r = t._post_tweet(text="x" * 281)
    assert r.success is False
    assert "280" in r.error

def test_twitter_tweet_exact_280_passes_length_check():
    t = TwitterTool(credentials=_creds_twitter())
    # HTTP will fail (no real server), but should NOT fail on length
    r = t._post_tweet(text="x" * 280)
    # Fails on HTTP, not on length validation
    assert r.error is None or "280" not in r.error


# ---------------------------------------------------------------------------
# TikTok — video file existence check
# ---------------------------------------------------------------------------

def test_tiktok_nonexistent_video_returns_error():
    t = TikTokTool(credentials=_creds_tiktok())
    r = t.run(action="upload_video", video_path="/nonexistent/video.mp4", caption="test")
    assert r.success is False
    assert "no existe" in r.error


# ---------------------------------------------------------------------------
# Instagram — successful post_image (mocked HTTP)
# ---------------------------------------------------------------------------

def test_instagram_post_image_success():
    t = InstagramTool(credentials=_creds_instagram())
    with patch.object(t, "_post_image") as mock_post:
        mock_post.return_value = t._success("Post publicado en Instagram. ID: 999", raw_data={"media_id": "999"})
        r = t.run(action="post_image", caption="hola", image_url="http://img.example.com/1.jpg")
    assert r.success is True
    assert "999" in r.output
    assert r.raw_data["media_id"] == "999"


# ---------------------------------------------------------------------------
# Facebook — successful post_text (mocked HTTP)
# ---------------------------------------------------------------------------

def test_facebook_post_text_success():
    t = FacebookTool(credentials=_creds_facebook())
    with patch("tools.social.facebook.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"id": "page_456_post_1"}
        r = t._post_text(message="Hola Facebook")
    assert r.success is True
    assert "page_456_post_1" in r.output


# ---------------------------------------------------------------------------
# LinkedIn — post_text with org_id uses org URN (mocked HTTP)
# ---------------------------------------------------------------------------

def test_linkedin_post_text_with_org_id():
    t = LinkedInTool(credentials=_creds_linkedin())
    with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
        instance = MockHTTP.return_value
        instance.post.return_value = {"id": "urn:li:share:123"}
        r = t._post_text(text="Contenido profesional")
    assert r.success is True
    assert r.raw_data["post_id"] == "urn:li:share:123"


# ---------------------------------------------------------------------------
# SMTP — send success (mocked smtplib)
# ---------------------------------------------------------------------------

def test_smtp_send_success():
    t = SMTPTool(credentials=_creds_smtp())
    mock_smtp = MagicMock()
    with patch("tools.email.smtp.smtplib.SMTP", return_value=mock_smtp):
        r = t._send(to="dest@example.com", subject="Test", body="Cuerpo")
    assert r.success is True
    assert "dest@example.com" in r.output
    mock_smtp.sendmail.assert_called_once()

def test_smtp_send_bulk_success():
    t = SMTPTool(credentials=_creds_smtp())
    mock_smtp = MagicMock()
    recipients = ["a@b.com", "c@d.com", "e@f.com"]
    with patch("tools.email.smtp.smtplib.SMTP", return_value=mock_smtp):
        r = t._send_bulk(recipients=recipients, subject="Bulk", body="Msg")
    assert r.success is True
    assert mock_smtp.sendmail.call_count == 3
    assert r.raw_data["sent"] == recipients
    assert r.raw_data["failed"] == []

def test_smtp_send_bulk_partial_failure():
    t = SMTPTool(credentials=_creds_smtp())
    mock_smtp = MagicMock()
    # Second sendmail call raises exception
    mock_smtp.sendmail.side_effect = [None, Exception("rejected"), None]
    recipients = ["a@b.com", "bad@fail.com", "c@d.com"]
    with patch("tools.email.smtp.smtplib.SMTP", return_value=mock_smtp):
        r = t._send_bulk(recipients=recipients, subject="S", body="B")
    assert r.success is True
    assert len(r.raw_data["sent"]) == 2
    assert len(r.raw_data["failed"]) == 1

def test_smtp_send_bulk_no_recipients_returns_error():
    t = SMTPTool(credentials=_creds_smtp())
    r = t._send_bulk(recipients=[], subject="S", body="B")
    assert r.success is False
    assert "recipients" in r.error

def test_smtp_send_connection_error():
    t = SMTPTool(credentials=_creds_smtp())
    with patch("tools.email.smtp.smtplib.SMTP", side_effect=Exception("connection refused")):
        r = t._send(to="x@y.com", subject="S", body="B")
    assert r.success is False
    assert "connection refused" in r.error
