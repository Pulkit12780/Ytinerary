from __future__ import annotations
from pydantic import BaseModel, field_validator
from typing import Literal, Optional


# ── Trip-type taxonomy (single source of truth — dev plan §2) ────────────────
# Shared by request validation, the sourcer query builder, and the intent prompts.

TripType = Literal["balanced", "romantic", "family", "adventure", "nature", "culture"]

TRIP_TYPES: tuple[TripType, ...] = (
    "balanced", "romantic", "family", "adventure", "nature", "culture",
)

# Search-query modifier per trip type. Appended to the base "<destination> ...
# travel vlog" query the sourcer builds. "balanced" adds nothing (current behavior).
TRIP_TYPE_SEARCH_MODIFIERS: dict[str, str] = {
    "balanced": "",
    "romantic": "honeymoon couples",
    "family": "with kids family",
    "adventure": "trekking adventure",
    "nature": "nature slow travel",
    "culture": "heritage culture history",
}

NOTES_MAX_LEN = 500


class PlanRequest(BaseModel):
    destination: str
    trip_type: TripType = "balanced"   # default preserves current behavior
    notes: Optional[str] = None        # free text, capped at NOTES_MAX_LEN
    youtube_urls: list[str] = []       # optional — auto-sourced when empty
    hotel: Optional[str] = None
    start_date: Optional[str] = None  # ISO YYYY-MM-DD
    end_date: Optional[str] = None    # ISO YYYY-MM-DD
    maps_links: Optional[list[str]] = None

    @field_validator("destination")
    @classmethod
    def destination_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("destination cannot be empty")
        return v

    @field_validator("notes")
    @classmethod
    def cap_notes(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        return v[:NOTES_MAX_LEN]

    @field_validator("youtube_urls")
    @classmethod
    def at_most_five_urls(cls, v: list[str]) -> list[str]:
        # Empty is valid now (auto-sourcing handles it). Cap manual input at 5.
        if len(v) > 5:
            raise ValueError("a maximum of 5 YouTube URLs is allowed")
        return v


class SourceVideo(BaseModel):
    url: str
    title: str


class Place(BaseModel):
    name: str
    lat: float
    lng: float
    category: Optional[str] = None
    rating: Optional[float] = None
    hours: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    place_id: Optional[str] = None
    source_videos: list[SourceVideo] = []
    # Itinerary semantics added by the augmenter / judge
    meal_type: Optional[str] = None    # "breakfast" | "lunch" | "dinner" | None (attraction)
    source: str = "video"              # "video" | "suggested"
    time_of_day: Optional[str] = None  # "Morning" | "Afternoon" | "Evening" — display ordering


class DayCluster(BaseModel):
    day_number: int
    date_label: str   # "Day 1" or "Monday, May 20"
    theme_label: str  # e.g. "Old City & Bazaars"
    places: list[Place]
    notes: Optional[str] = None  # judge's one-line rationale for the day


class HotelPin(BaseModel):
    name: str
    lat: float
    lng: float


class PlanResponse(BaseModel):
    destination: str
    clusters: list[DayCluster]
    more_to_explore: list[Place] = []
    unresolved_places: list[str] = []
    hotel: Optional[HotelPin] = None
    total_places: int
    video_titles: list[str] = []
    warnings: list[str] = []  # feasibility flags, e.g. "X is 40 km out — moved to More to Explore"


class ErrorResponse(BaseModel):
    error: str
    code: str   # ZERO_PLACES | MISSING_TRANSCRIPT | GEOCODING_FAILURE | INVALID_DESTINATION | NO_VIDEOS_FOUND
    detail: Optional[str] = None
