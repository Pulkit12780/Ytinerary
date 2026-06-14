"""F1 — PlanRequest contract validation (A1–A4)."""
import pytest
from pydantic import ValidationError

from backend.models import (
    PlanRequest,
    NOTES_MAX_LEN,
    TRIP_TYPES,
    TRIP_TYPE_SEARCH_MODIFIERS,
)


def test_youtube_urls_optional_and_empty_is_valid():
    # A3: zero URLs is now valid (auto-sourcing handles it).
    req = PlanRequest(destination="Jaipur")
    assert req.youtube_urls == []
    assert PlanRequest(destination="Jaipur", youtube_urls=[]).youtube_urls == []


def test_youtube_urls_max_five_cap_enforced():
    PlanRequest(destination="X", youtube_urls=[f"u{i}" for i in range(5)])  # ok
    with pytest.raises(ValidationError):
        PlanRequest(destination="X", youtube_urls=[f"u{i}" for i in range(6)])


def test_trip_type_defaults_to_balanced():
    assert PlanRequest(destination="Jaipur").trip_type == "balanced"


@pytest.mark.parametrize("tt", TRIP_TYPES)
def test_all_trip_types_accepted(tt):
    assert PlanRequest(destination="Jaipur", trip_type=tt).trip_type == tt


def test_invalid_trip_type_rejected():
    with pytest.raises(ValidationError):
        PlanRequest(destination="Jaipur", trip_type="luxury")


def test_notes_capped_at_500_and_stripped():
    # A2: cap at NOTES_MAX_LEN, strip; blank -> None.
    long = "x" * 600
    req = PlanRequest(destination="Jaipur", notes=long)
    assert len(req.notes) == NOTES_MAX_LEN
    assert PlanRequest(destination="Jaipur", notes="  hi  ").notes == "hi"
    assert PlanRequest(destination="Jaipur", notes="   ").notes is None
    assert PlanRequest(destination="Jaipur").notes is None


def test_destination_required_non_empty():
    with pytest.raises(ValidationError):
        PlanRequest(destination="   ")


def test_taxonomy_is_single_source_of_truth():
    # Every trip type has a search modifier (balanced may be empty).
    assert set(TRIP_TYPES) == set(TRIP_TYPE_SEARCH_MODIFIERS)
    assert TRIP_TYPE_SEARCH_MODIFIERS["balanced"] == ""
    assert TRIP_TYPE_SEARCH_MODIFIERS["family"]  # non-empty
