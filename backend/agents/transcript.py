"""Fetch YouTube transcripts via youtube-transcript-api with yt-dlp fallback."""
from __future__ import annotations
import re
import asyncio
from .. import cache


def _extract_video_id(url: str) -> str | None:
    patterns = [
        r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/)([a-zA-Z0-9_-]{11})",
        r"(?:shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def _fetch_via_api(video_id: str) -> tuple[str, None] | tuple[None, str]:
    """Returns (transcript_text, None) or (None, error_reason).

    Priority:
      1. English captions (manual or auto-generated)
      2. Any other language translated to English
      3. Any other language raw (GPT still extracts place names from Hindi etc.)
    Uses youtube-transcript-api v1.x instance API.
    """
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
    )

    api = YouTubeTranscriptApi()

    def _entries_to_text(fetched) -> str:
        return " ".join(e["text"] for e in fetched.to_raw_data())

    try:
        # 1. Try English directly
        try:
            fetched = api.fetch(video_id, languages=("en", "en-US", "en-GB"))
            return _entries_to_text(fetched), None
        except NoTranscriptFound:
            pass

        # 2. List all transcripts and fall back gracefully
        transcript_list = api.list(video_id)

        # Try any transcript, preferring translatable ones
        target = None
        for t in transcript_list:
            if t.is_translatable:
                target = t
                break
        if target is None:
            # grab whatever is available
            for t in transcript_list:
                target = t
                break

        if target is None:
            return None, "no_transcript"

        try:
            fetched = target.translate("en").fetch()
        except Exception:
            fetched = target.fetch()   # raw language — GPT handles place names fine

        return _entries_to_text(fetched), None

    except TranscriptsDisabled:
        return None, "no_transcript"
    except VideoUnavailable:
        return None, "video_unavailable"
    except Exception:
        return None, "api_error"


def _fetch_via_ytdlp(url: str) -> dict:
    """Returns {title, transcript, error}. Uses description as transcript fallback."""
    try:
        import yt_dlp
    except ImportError:
        return {"title": None, "transcript": None, "error": "yt_dlp_missing"}

    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        title = info.get("title", "")
        description = info.get("description", "")
        return {
            "title": title,
            "transcript": description if description else None,
            "error": None if description else "no_description",
        }
    except Exception as exc:
        return {"title": None, "transcript": None, "error": str(exc)[:120]}


async def fetch_transcript(url: str) -> dict:
    """
    Returns:
      {url, video_id, title, transcript, error}
    error is None on success, or a short code string on failure.
    """
    cached = cache.get(url)
    if cached:
        return cached

    video_id = _extract_video_id(url)
    if not video_id:
        return {"url": url, "video_id": None, "title": None, "transcript": None, "error": "invalid_url"}

    # Primary: youtube-transcript-api (fast, clean text)
    transcript_text, api_error = await asyncio.to_thread(_fetch_via_api, video_id)

    if transcript_text:
        # Get title via yt-dlp metadata (best-effort, don't fail the pipeline)
        try:
            ytdlp_data = await asyncio.to_thread(_fetch_via_ytdlp, url)
            title = ytdlp_data.get("title") or video_id
        except Exception:
            title = video_id

        result = {"url": url, "video_id": video_id, "title": title, "transcript": transcript_text, "error": None}
        cache.set(url, result)
        return result

    # Fallback: yt-dlp metadata + description
    ytdlp_data = await asyncio.to_thread(_fetch_via_ytdlp, url)
    result = {
        "url": url,
        "video_id": video_id,
        "title": ytdlp_data.get("title") or video_id,
        "transcript": ytdlp_data.get("transcript"),
        "error": ytdlp_data.get("error") or api_error,
    }
    if result["transcript"]:
        result["error"] = None
        cache.set(url, result)
    return result
