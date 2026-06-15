"""Extract place names from video transcripts using OpenAI."""
from __future__ import annotations
import json
import os
import asyncio
from openai import OpenAI, APIError

_client: OpenAI | None = None
_MODEL = "gpt-4o-mini"

_SYSTEM = """\
You are a travel place extractor. Given a YouTube travel video transcript (or its \
description, which may be promotional) and a destination, extract only the specific, \
*visitable* places a traveler would actually go to.

Return ONLY a valid JSON object — no explanation, no markdown:
{
  "places": [
    {"name": "Place Name", "category": "attraction"|"food"|"market"|"viewpoint"|"museum"|"temple"|"beach"|"neighbourhood"|"park"|"nature"|"other", "scope": "poi"|"district"|"town"|"region", "sentiment": "positive"|"neutral"|"negative", "context": "one brief phrase"}
  ]
}

Rules:
- Extract specific named places a traveler visits for enjoyment: restaurants, cafes,
  attractions, neighbourhoods, markets, viewpoints, temples, museums, beaches, parks,
  nature spots, landmarks.
- Use "food" for any restaurant, cafe, bakery, street-food spot, bar or eatery — this
  matters for meal planning.
- NEVER extract: airports, ports/harbours, bus or train stations, government or
  administrative offices, hospitals, banks, hotels-as-sights, residential areas,
  business parks, or the creator's own shop/brand/sponsor mentioned in the video.
- Skip vague references ("a nice restaurant", "some street", "a local spot").
- Set "scope": "poi" for a single visitable spot; "district" for a neighbourhood/area;
  "town" for a whole town/city; "region" for a province/island/country. A town or region
  is NOT a stop on its own — only extract it if it's clearly named as a place to base in.
- Skip the destination itself (the searched city/country) unless it names a specific
  district within it.
- Negative-sentiment places are kept in output (caller will filter them).
- Use the common English name, not a translation. Deduplicate repeated mentions.
"""

_MAX_TRANSCRIPT = 10_000  # characters sent to the model


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
            response_format={"type": "json_object"},
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
