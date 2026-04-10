"""Tests for tools/media/: LocalImageGenTool, VideoGenTool."""
from unittest.mock import MagicMock, patch, mock_open
import base64

import pytest
import httpx  # ensure module is loaded so patching works

from tools.media.image_gen_local import LocalImageGenTool
from tools.media.video_gen import VideoGenTool
from tools.base import ToolRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _creds_sd():
    return {}  # No mandatory credentials — host defaults to localhost:7860


def _make_png_b64() -> str:
    # 1x1 white PNG (minimal valid PNG bytes)
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
        b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18"
        b"\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return base64.b64encode(png_bytes).decode()


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def test_media_tools_registered():
    names = [t["name"] for t in ToolRegistry.list_all()]
    for name in ("image_gen_local", "video_gen"):
        assert name in names


# ---------------------------------------------------------------------------
# LocalImageGenTool — availability check
# ---------------------------------------------------------------------------

def test_image_gen_check_not_available():
    t = LocalImageGenTool(credentials={})
    with patch.object(t, "_is_available", return_value=False):
        r = t.run(action="check")
    assert r.success is False
    assert "no disponible" in r.error


def test_image_gen_check_available():
    t = LocalImageGenTool(credentials={})
    mock_resp = MagicMock()
    mock_resp.json.return_value = [
        {"title": "v1-5-pruned.ckpt"},
        {"title": "sd-xl-base-1.0.safetensors"},
    ]
    mock_resp.status_code = 200

    with patch("httpx.get", return_value=mock_resp):
        r = t.run(action="check")

    assert r.success is True
    assert "disponible" in r.output
    assert "models" in r.raw_data


# ---------------------------------------------------------------------------
# LocalImageGenTool — generate
# ---------------------------------------------------------------------------

def test_image_gen_generate_empty_prompt_returns_error():
    t = LocalImageGenTool(credentials={})
    r = t.run(action="generate", prompt="")
    assert r.success is False
    assert "prompt" in r.error


def test_image_gen_generate_sd_not_available_returns_error():
    t = LocalImageGenTool(credentials={})
    with patch.object(t, "_is_available", return_value=False):
        r = t.run(action="generate", prompt="a cat in space")
    assert r.success is False
    assert "no disponible" in r.error


def test_image_gen_generate_success(tmp_path):
    t = LocalImageGenTool(credentials={})
    png_b64 = _make_png_b64()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"images": [png_b64]}
    mock_resp.raise_for_status.return_value = None

    out = str(tmp_path / "test_image.png")

    with patch.object(t, "_is_available", return_value=True):
        with patch("httpx.post", return_value=mock_resp):
            r = t._generate(prompt="a cat in space", output_path=out)

    assert r.success is True
    assert out in r.output
    assert r.raw_data["path"] == out


def test_image_gen_generate_no_images_returned():
    t = LocalImageGenTool(credentials={})
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"images": []}
    mock_resp.raise_for_status.return_value = None

    with patch.object(t, "_is_available", return_value=True):
        with patch("httpx.post", return_value=mock_resp):
            r = t._generate(prompt="a dog", output_path="/tmp/out.png")

    assert r.success is False
    assert "no devolvió" in r.error


def test_image_gen_generate_auto_output_path(tmp_path):
    t = LocalImageGenTool(credentials={})
    png_b64 = _make_png_b64()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"images": [png_b64]}
    mock_resp.raise_for_status.return_value = None

    # Use a real tmp_path so Path.mkdir works; only mock httpx
    out = str(tmp_path / "auto_output.png")
    with patch.object(t, "_is_available", return_value=True):
        with patch("httpx.post", return_value=mock_resp):
            r = t._generate(prompt="a landscape painting", output_path=out)

    assert r.success is True
    assert r.raw_data["path"] == out


def test_image_gen_http_error_returns_error():
    t = LocalImageGenTool(credentials={})
    with patch.object(t, "_is_available", return_value=True):
        with patch("httpx.post", side_effect=Exception("timeout")):
            r = t._generate(prompt="a sunset")
    assert r.success is False
    assert "timeout" in r.error


def test_image_gen_unsupported_action():
    t = LocalImageGenTool(credentials={})
    r = t.run(action="delete_image")
    assert r.success is False
    assert "no soportada" in r.error


def test_image_gen_custom_host():
    t = LocalImageGenTool(credentials={"host": "http://192.168.1.100:7860"})
    assert t._get_host() == "http://192.168.1.100:7860"


def test_image_gen_default_host():
    t = LocalImageGenTool(credentials={})
    assert t._get_host() == "http://localhost:7860"


# ---------------------------------------------------------------------------
# VideoGenTool — availability check
# ---------------------------------------------------------------------------

def test_video_gen_check_not_available():
    t = VideoGenTool(credentials={})
    with patch.object(t, "_is_available", return_value=False):
        r = t.run(action="check")
    assert r.success is False
    assert "no disponible" in r.error


def test_video_gen_check_available():
    t = VideoGenTool(credentials={})
    with patch.object(t, "_is_available", return_value=True):
        r = t.run(action="check")
    assert r.success is True
    assert "disponible" in r.output


# ---------------------------------------------------------------------------
# VideoGenTool — generate
# ---------------------------------------------------------------------------

def test_video_gen_generate_empty_prompt_returns_error():
    t = VideoGenTool(credentials={})
    r = t.run(action="generate", prompt="")
    assert r.success is False
    assert "prompt" in r.error


def test_video_gen_generate_not_available_returns_error():
    t = VideoGenTool(credentials={})
    with patch.object(t, "_is_available", return_value=False):
        r = t.run(action="generate", prompt="ocean waves")
    assert r.success is False
    assert "no disponible" in r.error


def test_video_gen_generate_no_frames_returned():
    t = VideoGenTool(credentials={})
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"images": []}
    mock_resp.raise_for_status.return_value = None

    with patch.object(t, "_is_available", return_value=True):
        with patch("httpx.post", return_value=mock_resp):
            r = t._generate(prompt="ocean waves", output_path="/tmp/out.mp4")

    assert r.success is False
    assert "no devolvió" in r.error


def test_video_gen_generate_success(tmp_path):
    t = VideoGenTool(credentials={})
    png_b64 = _make_png_b64()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"images": [png_b64, png_b64, png_b64]}
    mock_resp.raise_for_status.return_value = None

    out = str(tmp_path / "test_video.mp4")
    ffmpeg_result = MagicMock()
    ffmpeg_result.returncode = 0

    with patch.object(t, "_is_available", return_value=True):
        with patch("httpx.post", return_value=mock_resp):
            with patch("subprocess.run", return_value=ffmpeg_result):
                r = t._generate(prompt="ocean waves", output_path=out)

    assert r.success is True
    assert out in r.output
    assert r.raw_data["frames"] == 3


def test_video_gen_ffmpeg_error_returns_error(tmp_path):
    t = VideoGenTool(credentials={})
    png_b64 = _make_png_b64()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"images": [png_b64]}
    mock_resp.raise_for_status.return_value = None

    out = str(tmp_path / "fail_video.mp4")
    ffmpeg_result = MagicMock()
    ffmpeg_result.returncode = 1
    ffmpeg_result.stderr = b"ffmpeg error: codec not found"

    with patch.object(t, "_is_available", return_value=True):
        with patch("httpx.post", return_value=mock_resp):
            with patch("subprocess.run", return_value=ffmpeg_result):
                r = t._generate(prompt="test", output_path=out)

    assert r.success is False
    assert "ffmpeg" in r.error


# ---------------------------------------------------------------------------
# VideoGenTool — img2vid
# ---------------------------------------------------------------------------

def test_video_gen_img2vid_empty_path_returns_error():
    t = VideoGenTool(credentials={})
    r = t.run(action="img2vid", image_path="")
    assert r.success is False
    assert "image_path" in r.error


def test_video_gen_img2vid_nonexistent_file_returns_error():
    t = VideoGenTool(credentials={})
    r = t.run(action="img2vid", image_path="/nonexistent/image.jpg")
    assert r.success is False
    assert "no encontrado" in r.error


def test_video_gen_img2vid_not_available_returns_error(tmp_path):
    img = tmp_path / "frame.png"
    img.write_bytes(b"fake-png-bytes")
    t = VideoGenTool(credentials={})

    with patch.object(t, "_is_available", return_value=False):
        r = t.run(action="img2vid", image_path=str(img))

    assert r.success is False
    assert "no disponible" in r.error


def test_video_gen_img2vid_success(tmp_path):
    img = tmp_path / "frame.png"
    img.write_bytes(b"fake-png-bytes")
    t = VideoGenTool(credentials={})

    png_b64 = _make_png_b64()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"images": [png_b64, png_b64]}
    mock_resp.raise_for_status.return_value = None

    out = str(tmp_path / "animated.mp4")
    ffmpeg_result = MagicMock()
    ffmpeg_result.returncode = 0

    with patch.object(t, "_is_available", return_value=True):
        with patch("httpx.post", return_value=mock_resp):
            with patch("subprocess.run", return_value=ffmpeg_result):
                r = t._img2vid(image_path=str(img), output_path=out)

    assert r.success is True
    assert "animated" in r.output or out in r.output


def test_video_gen_unsupported_action():
    t = VideoGenTool(credentials={})
    r = t.run(action="delete_video")
    assert r.success is False
    assert "no soportada" in r.error
