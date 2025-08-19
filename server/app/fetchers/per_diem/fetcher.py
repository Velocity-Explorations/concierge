from __future__ import annotations

from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
import datetime as dt
import requests

# ---------- Your models ----------

class StayModel(BaseModel):
    days: int = Field(..., ge=1, description="Number of days for meal requests")
    location: str = Field(..., description="Location for meal requests")

class PerDiemRequest(BaseModel):
    stays: List[StayModel]

class StayCostModel(BaseModel):
    location: str = Field(..., description="Location for lodging requests")
    meal_cost: float = Field(..., ge=0, description="Total cost for meals")
    lodging_cost: float = Field(..., ge=0, description="Total cost for lodging")
    total_cost: float = Field(..., ge=0, description="Total cost for the stay")

class PerDiemResponse(BaseModel):
    costs: list[StayCostModel] = Field(..., description="List of costs for each stay")

INTL_DOMESTIC_SAME_COUNTRY = 40.0   # per-day
INTL_OTHER = 80.0                   # per-day (between-country default, used as general intl default)
ETHIOPIA_FLAT = 25.0                # per-day, covers meals/incidentals/lodging per note

# ---------- Core daily calculation (meals only, per policy) ----------

def _daily_meals_amount_for_location(location: str, gsa_api_key: Optional[str] = None) -> float:
    """
    Implements your 'Meals' policy for a single stay location.
    - U.S.: GSA M&IE (capped at $80).
    - Ethiopia: $25/day flat (covers M/I/L; we attribute it to meal_cost due to schema).
    - Cameroon / Philippines: raise for currency/tier handling (not implemented here).
    - All other non-US: default to $80/day (international) as a general safe policy,
      or $40/day if you prefer to treat single-location stays as 'domestic within country'.
      Here we use $80/day as the default to align with 'international between other countries'.
    """
    city, state, country = _parse_location(location)

    # Normalize missing country for US patterns like "City, CA"
    if country is None and state in US_STATE_CODES:
        country = "united states"

    # U.S.
    if _is_us(country):
        return _fetch_gsa_mie(city, state, dt.date.today(), api_key=gsa_api_key)

    # Explicit exceptions
    if (country or "").lower() == "ethiopia":
        return ETHIOPIA_FLAT

    if (country or "").lower() == "cameroon":
        raise ValueError("Cameroon uses 40,000 XAF/day (no deductions). Add FX conversion before computing USD.")

    if (country or "").lower() == "philippines":
        raise ValueError("Philippines uses fixed PHP tiers. Provide tier/FX or extend the function to handle PHP.")

    # Countries requiring DSSR with deductions (not implemented here)
    # Kenya, Tanzania, Nigeria, Malaysia, Vietnam -> would call a DSSR fetcher.
    # For now, use the general international default ($80/day).
    return INTL_OTHER

# ---------- Public entrypoint ----------

def get_per_diem_estimate(request: PerDiemRequest, gsa_api_key: Optional[str] = None) -> PerDiemResponse:
    """
    Entry point: takes PerDiemRequest and returns PerDiemResponse.
    - Computes meal_cost per stay per policy.
    - lodging_cost is 0.0 (policy input was 'Meals'; lodging not computed here).
    - total_cost = meal_cost + lodging_cost.
    """
    costs: List[StayCostModel] = []

    for stay in request.stays:
        daily_amount = _daily_meals_amount_for_location(stay.location, gsa_api_key=gsa_api_key)
        meal_cost_total = round(daily_amount * stay.days, 2)
        lodging_cost_total = 0.0  # Not computed in this function; adjust when lodging policy is added.
        total = round(meal_cost_total + lodging_cost_total, 2)

        costs.append(
            StayCostModel(
                location=stay.location,
                meal_cost=meal_cost_total,
                lodging_cost=lodging_cost_total,
                total_cost=total,
            )
        )

    return PerDiemResponse(costs=costs)