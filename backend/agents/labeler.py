"""Label day clusters with evocative names using OpenAI."""
from __future__ import annotations
import json
import os
import asyncio
from datetime import date, timedelta
from openai import OpenAI

_client: OpenAI | None = None
_MODEL = "gpt-4o-mini"


def _day_date_labels(
    num_clusters: int, start_date: str | None
) -> list[str]:
    """Returns ["Day 1", "Day 2", ...] or ["Monday May 20", ...] if start_date given."""
    if start_date:
        try:
            d = date.fromisoformat(start_date)
            return [
                (d + timedelta(days=i)).strftime("%A, %b %-d")
                for i in range(num_clusters)
            ]
        except ValueError:
            pass
    return [f"Day {i + 1}" for i in range(num_clusters)]


async def label_clusters(
    clusters: list[list[dict]],
    destination: str,
    start_date: str | None = None,
) -> list[str]:
    """
    Returns a list of short theme labels, one per cluster.
    E.g. ["Old City & Bazaars", "Coastal Walks & Seafood", ...]
    Never raises — falls back to generic labels on failure.
    """
    global _client
    if not clusters:
        return []

    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    summaries = "\n".join(
        f"Cluster {i + 1}: {', '.join(p['name'] for p in cluster)}"
        for i, cluster in enumerate(clusters)
    )

    prompt = (
        f"Destination: {destination}\n\n"
        f"Geographic clusters of places:\n{summaries}\n\n"
        f"Write a short, evocative theme label for each cluster "
        f"(3-6 words, e.g. 'Old City & Bazaars', 'Coastal Walks & Seafood').\n"
        f"Return ONLY valid JSON: {{\"labels\": [\"...\", \"...\"]}}"
    )

    try:
        response = await asyncio.to_thread(
            _client.chat.completions.create,
            model=_MODEL,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        labels = data.get("labels", [])
        # Pad or trim to match cluster count
        while len(labels) < len(clusters):
            labels.append(f"Cluster {len(labels) + 1}")
        return labels[: len(clusters)]
    except Exception:
        return [f"Cluster {i + 1}" for i in range(len(clusters))]


def make_date_labels(num_clusters: int, start_date: str | None) -> list[str]:
    return _day_date_labels(num_clusters, start_date)
