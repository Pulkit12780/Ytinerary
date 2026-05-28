"""Extract place names from video transcripts using OpenAI."""
from __future__ import annotations
import json
import os
import asyncio
from openai import OpenAI, APIError

_client: OpenAI | None = None
_MODEL = "gpt-4o-mini"

_SYSTEM = """\
You are a travel place extractor. Given a YouTube travel video transcript and a destination, \
extract all specific named places mentioned.

Return ONLY a valid JSON object — no explanation, no markdown:
{
  "places": [
    {"name": "Place Name", "sentiment": "positive"|"neutral"|"negative", "context": "one brief phrase"}
  ]
}

Rules:
- Extract specific named places only: restaurants, cafes, attractions, neighbourhoods, markets, viewpoints, hotels, temples, museums, beaches, etc.
- Skip vague references like "a nice restaurant", "some street", "a local spot"
- Skip the destination city or country itself unless it names a very specific district/area
- Negative-sentiment places are kept in output (caller will filter them)
- Each place name should be the common English name, not a translation
- Deduplicate: if a place is mentioned several times, include it once
"""

_MAX_TRANSCRIPT = 10_000  # characters sent to Haiku


async def extract_places(transcript: str, destination: str, title: str = "") -> list[dict]:
    """
    Returns list of dicts: {name, sentiment, context}.
    Never raises — returns [] on any failure.
    """
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = (
        f"Destination: {destination}\n"
        f"Video title: {title or 'unknown'}\n\n"
        f"Transcript (may be truncated):\n{transcript[:_MAX_TRANSCRIPT]}"
    )

    try:
        response = await asyncio.to_thread(
            _client.chat.completions.create,
            model=_MODEL,
            max_tokens=2048,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": prompt},
            ],
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        return data.get("places", [])
    except (json.JSONDecodeError, KeyError, IndexError, APIError):
        return []
