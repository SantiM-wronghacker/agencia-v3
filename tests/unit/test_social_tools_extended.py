"""Extended tests for social tools — covers HTTP success & error paths."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from tools.social.instagram import InstagramTool
from tools.social.facebook import FacebookTool
from tools.social.linkedin import LinkedInTool
from tools.social.tiktok import TikTokTool
from tools.social.twitter import TwitterTool


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_IG_CREDS = {"access_token": "tok-123", "account_id": "acc-456"}
_FB_CREDS = {"page_token": "page-tok", "page_id": "page-123"}
_LI_CREDS = {"access_token": "li-tok", "org_id": "org-789"}
_TT_CREDS = {"access_token": "tt-tok", "open_id": "open-123"}
_TW_CREDS = {"bearer_token": "tw-bear-tok"}


# ===========================================================================
# InstagramTool
# ===========================================================================

class TestInstagramTool:

    # --- post_image success path ---
    def test_post_image_success(self, tmp_path):
        with patch("tools.social.instagram.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            # First POST: create container → returns creation_id
            # Second POST: publish → returns media_id
            mock_client.post.side_effect = [
                {"id": "container-001"},
                {"id": "media-001"},
            ]
            tool = InstagramTool(_IG_CREDS)
            result = tool.run(action="post_image", caption="Hola mundo",
                              image_url="https://example.com/img.jpg")

        assert result.success
        assert "media-001" in result.output

    def test_post_image_container_fails(self):
        with patch("tools.social.instagram.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None  # HTTP error
            tool = InstagramTool(_IG_CREDS)
            result = tool.run(action="post_image", caption="test")

        assert not result.success
        assert result.error is not None

    def test_post_image_publish_fails(self):
        with patch("tools.social.instagram.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.side_effect = [
                {"id": "container-001"},
                None,  # publish fails
            ]
            tool = InstagramTool(_IG_CREDS)
            result = tool.run(action="post_image", caption="test")

        assert not result.success

    def test_post_image_no_access_token(self):
        tool = InstagramTool({"account_id": "acc-456"})
        result = tool.run(action="post_image")
        assert not result.success
        assert "access_token" in result.error

    def test_post_image_no_account_id(self):
        tool = InstagramTool({"access_token": "tok"})
        result = tool.run(action="post_image")
        assert not result.success
        assert "account_id" in result.error

    # --- get_account success path ---
    def test_get_account_success(self):
        with patch("tools.social.instagram.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "name": "Mi Marca", "followers_count": 5000, "media_count": 42
            }
            tool = InstagramTool(_IG_CREDS)
            result = tool.run(action="get_account")

        assert result.success
        assert "Mi Marca" in result.output
        assert "5000" in result.output

    def test_get_account_http_error(self):
        with patch("tools.social.instagram.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = InstagramTool(_IG_CREDS)
            result = tool.run(action="get_account")

        assert not result.success

    # --- get_stats success path ---
    def test_get_stats_success(self):
        with patch("tools.social.instagram.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "data": [
                    {"name": "impressions", "values": [{"value": 1200}]},
                    {"name": "reach", "values": [{"value": 800}]},
                ]
            }
            tool = InstagramTool(_IG_CREDS)
            result = tool.run(action="get_stats", media_id="media-001")

        assert result.success
        assert "impressions" in result.output

    def test_get_stats_no_media_id(self):
        tool = InstagramTool(_IG_CREDS)
        result = tool.run(action="get_stats")
        assert not result.success
        assert "media_id" in result.error

    def test_get_stats_http_error(self):
        with patch("tools.social.instagram.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = InstagramTool(_IG_CREDS)
            result = tool.run(action="get_stats", media_id="media-001")

        assert not result.success

    def test_unknown_action(self):
        tool = InstagramTool(_IG_CREDS)
        result = tool.run(action="unknown_action")
        assert not result.success


# ===========================================================================
# FacebookTool
# ===========================================================================

class TestFacebookTool:

    def test_post_text_success(self):
        with patch("tools.social.facebook.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "post-123"}
            tool = FacebookTool(_FB_CREDS)
            result = tool.run(action="post_text", message="Hola desde Facebook")

        assert result.success
        assert "post-123" in result.output

    def test_post_text_http_error(self):
        with patch("tools.social.facebook.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = FacebookTool(_FB_CREDS)
            result = tool.run(action="post_text", message="test")

        assert not result.success

    def test_post_text_no_page_token(self):
        tool = FacebookTool({"page_id": "123"})
        result = tool.run(action="post_text")
        assert not result.success
        assert "page_token" in result.error

    def test_post_text_no_page_id(self):
        tool = FacebookTool({"page_token": "tok"})
        result = tool.run(action="post_text")
        assert not result.success
        assert "page_id" in result.error

    def test_post_image_success(self):
        with patch("tools.social.facebook.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "photo-456"}
            tool = FacebookTool(_FB_CREDS)
            result = tool.run(action="post_image", message="foto",
                              image_url="https://img.example.com/a.jpg")

        assert result.success
        assert "photo-456" in result.output

    def test_post_image_http_error(self):
        with patch("tools.social.facebook.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"wrong": "key"}
            tool = FacebookTool(_FB_CREDS)
            result = tool.run(action="post_image", message="test")

        assert not result.success

    def test_get_insights_success(self):
        with patch("tools.social.facebook.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "data": [
                    {"name": "page_fans", "values": [{"value": 1000}, {"value": 1050}]},
                ]
            }
            tool = FacebookTool(_FB_CREDS)
            result = tool.run(action="get_insights")

        assert result.success
        assert "page_fans" in result.output

    def test_get_insights_http_error(self):
        with patch("tools.social.facebook.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = FacebookTool(_FB_CREDS)
            result = tool.run(action="get_insights")

        assert not result.success

    def test_unknown_action(self):
        tool = FacebookTool(_FB_CREDS)
        result = tool.run(action="nope")
        assert not result.success


# ===========================================================================
# LinkedInTool
# ===========================================================================

class TestLinkedInTool:

    def test_post_text_with_org_id_success(self):
        with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "urn:li:ugcPost:789"}
            tool = LinkedInTool(_LI_CREDS)
            result = tool.run(action="post_text", text="Contenido profesional")

        assert result.success
        assert "LinkedIn" in result.output

    def test_post_text_via_me_endpoint(self):
        creds = {"access_token": "li-tok"}  # no org_id → uses /v2/me
        with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            # First call: GET /v2/me → returns user id
            # Second call: POST /v2/ugcPosts → returns post id
            mock_client.get.return_value = {"id": "person-abc"}
            mock_client.post.return_value = {"id": "urn:li:ugcPost:999"}
            tool = LinkedInTool(creds)
            result = tool.run(action="post_text", text="Texto")

        assert result.success

    def test_post_text_me_endpoint_fails(self):
        creds = {"access_token": "li-tok"}
        with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None  # /v2/me fails
            tool = LinkedInTool(creds)
            result = tool.run(action="post_text", text="Texto")

        assert not result.success

    def test_post_text_no_access_token(self):
        tool = LinkedInTool({"org_id": "123"})
        result = tool.run(action="post_text", text="test")
        assert not result.success
        assert "access_token" in result.error

    def test_post_text_http_error(self):
        with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = LinkedInTool(_LI_CREDS)
            result = tool.run(action="post_text", text="test")

        assert not result.success

    def test_post_image_success(self):
        with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"id": "urn:li:ugcPost:img001"}
            tool = LinkedInTool(_LI_CREDS)
            result = tool.run(action="post_image", text="imagen",
                              image_url="https://img.example.com/li.jpg")

        assert result.success

    def test_post_image_http_error(self):
        with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = LinkedInTool(_LI_CREDS)
            result = tool.run(action="post_image", text="img")

        assert not result.success

    def test_get_stats_success(self):
        with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "elements": [{"totalFollowerCount": 2500, "organicFollowerCount": 2000}]
            }
            tool = LinkedInTool(_LI_CREDS)
            result = tool.run(action="get_stats")

        assert result.success
        assert "2500" in result.output

    def test_get_stats_no_org_id(self):
        tool = LinkedInTool({"access_token": "tok"})
        result = tool.run(action="get_stats")
        assert not result.success
        assert "org_id" in result.error

    def test_get_stats_http_error(self):
        with patch("tools.social.linkedin.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = LinkedInTool(_LI_CREDS)
            result = tool.run(action="get_stats")

        assert not result.success

    def test_unknown_action(self):
        tool = LinkedInTool(_LI_CREDS)
        result = tool.run(action="unknown")
        assert not result.success


# ===========================================================================
# TikTokTool
# ===========================================================================

class TestTikTokTool:

    def test_upload_video_success(self, tmp_path):
        video_file = tmp_path / "video.mp4"
        video_file.write_bytes(b"fake video data")

        with patch("tools.social.tiktok.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"data": {"publish_id": "pub-001"}}
            tool = TikTokTool(_TT_CREDS)
            result = tool.run(action="upload_video",
                              video_path=str(video_file),
                              caption="Mi video",
                              hashtags=["viral", "trending"])

        assert result.success
        assert "pub-001" in result.output

    def test_upload_video_with_hashtags_in_title(self, tmp_path):
        video_file = tmp_path / "v.mp4"
        video_file.write_bytes(b"data")
        with patch("tools.social.tiktok.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"data": {"publish_id": "pub-002"}}
            tool = TikTokTool(_TT_CREDS)
            result = tool.run(action="upload_video",
                              video_path=str(video_file),
                              caption="Video",
                              hashtags=["hashtag1"])
        assert result.success

    def test_upload_video_http_error(self, tmp_path):
        video_file = tmp_path / "v.mp4"
        video_file.write_bytes(b"data")
        with patch("tools.social.tiktok.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = TikTokTool(_TT_CREDS)
            result = tool.run(action="upload_video", video_path=str(video_file))

        assert not result.success

    def test_upload_video_no_access_token(self, tmp_path):
        tool = TikTokTool({"open_id": "id"})
        result = tool.run(action="upload_video", video_path=str(tmp_path))
        assert not result.success
        assert "access_token" in result.error

    def test_upload_video_no_open_id(self, tmp_path):
        tool = TikTokTool({"access_token": "tok"})
        result = tool.run(action="upload_video", video_path=str(tmp_path))
        assert not result.success
        assert "open_id" in result.error

    def test_get_stats_success(self):
        with patch("tools.social.tiktok.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {
                "data": {
                    "videos": [
                        {"view_count": 5000, "like_count": 300, "comment_count": 25}
                    ]
                }
            }
            tool = TikTokTool(_TT_CREDS)
            result = tool.run(action="get_stats", video_id="vid-001")

        assert result.success
        assert "5000" in result.output

    def test_get_stats_no_video_id(self):
        tool = TikTokTool(_TT_CREDS)
        result = tool.run(action="get_stats")
        assert not result.success
        assert "video_id" in result.error

    def test_get_stats_http_error(self):
        with patch("tools.social.tiktok.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = TikTokTool(_TT_CREDS)
            result = tool.run(action="get_stats", video_id="vid-001")

        assert not result.success

    def test_unknown_action(self):
        tool = TikTokTool(_TT_CREDS)
        result = tool.run(action="nope")
        assert not result.success


# ===========================================================================
# TwitterTool
# ===========================================================================

class TestTwitterTool:

    def test_post_tweet_success(self):
        with patch("tools.social.twitter.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = {"data": {"id": "tw-001"}}
            tool = TwitterTool(_TW_CREDS)
            result = tool.run(action="post_tweet", text="Hola Twitter!")

        assert result.success
        assert "tw-001" in result.output

    def test_post_tweet_over_280_chars(self):
        tool = TwitterTool(_TW_CREDS)
        long_text = "x" * 281
        result = tool.run(action="post_tweet", text=long_text)
        assert not result.success
        assert "280" in result.error

    def test_post_tweet_http_error(self):
        with patch("tools.social.twitter.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.post.return_value = None
            tool = TwitterTool(_TW_CREDS)
            result = tool.run(action="post_tweet", text="test")

        assert not result.success

    def test_post_tweet_no_bearer_token(self):
        tool = TwitterTool({})
        result = tool.run(action="post_tweet", text="test")
        assert not result.success
        assert "bearer_token" in result.error

    def test_get_stats_success(self):
        with patch("tools.social.twitter.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = {
                "data": {
                    "public_metrics": {
                        "like_count": 42,
                        "retweet_count": 7,
                        "reply_count": 3,
                        "impression_count": 1500,
                    }
                }
            }
            tool = TwitterTool(_TW_CREDS)
            result = tool.run(action="get_stats", tweet_id="tw-001")

        assert result.success
        assert "42" in result.output
        assert "1500" in result.output

    def test_get_stats_no_tweet_id(self):
        tool = TwitterTool(_TW_CREDS)
        result = tool.run(action="get_stats")
        assert not result.success
        assert "tweet_id" in result.error

    def test_get_stats_http_error(self):
        with patch("tools.social.twitter.HTTPClient") as MockHTTP:
            mock_client = MagicMock()
            MockHTTP.return_value = mock_client
            mock_client.get.return_value = None
            tool = TwitterTool(_TW_CREDS)
            result = tool.run(action="get_stats", tweet_id="tw-001")

        assert not result.success

    def test_unknown_action(self):
        tool = TwitterTool(_TW_CREDS)
        result = tool.run(action="unknown")
        assert not result.success
