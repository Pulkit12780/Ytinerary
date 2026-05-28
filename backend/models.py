from __future__ import annotations
from pydantic import BaseModel, field_validator
from typing import Optional


class PlanRequest(BaseModel):
    destination: str
    youtube_urls: list[str]
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

    @field_validator("youtube_urls")
    @classmethod
    def at_least_one_url(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("at least one YouTube URL is required")
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
    foursquare_id: Optional[str] = None
    source_videos: list[SourceVideo] = []


class DayCluster(BaseModel):
    day_number: int
    date_label: str   # "Day 1" or "Monday, May 20"
    theme_label: str  # e.g. "Old City & Bazaars"
    places: list[Place]


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


class ErrorResponse(BaseModel):
    error: str
    code: str   # ZERO_PLACES | MISSING_TRANSCRIPT | GEOCODING_FAILURE | INVALID_DESTINATION
    detail: Optional[str] = None
