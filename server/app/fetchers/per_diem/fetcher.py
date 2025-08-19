from __future__ import annotations
from typing import List, Literal, Optional, Tuple
from pydantic import BaseModel, Field
import unicodedata
import datetime as dt

from server.app.fetchers.per_diem._types import CountryCode, USStateCode
from server.app.fetchers.per_diem.scrapers.dssr import fetch_dos_per_diem
from server.app.fetchers.per_diem.scrapers.exchange_rate import Currency, convert_to_currency
from server.app.fetchers.per_diem.scrapers.gsa import fetch_gsa_mie

# ---------- Models ----------

class USLocation(BaseModel):
    kind: Literal["us"] = "us"
    country: Literal[CountryCode.UNITED_STATES]
    state: USStateCode
    city: str = Field(..., description="City name")

class ForeignLocation(BaseModel):
    kind: Literal["foreign"] = "foreign"
    country: CountryCode
    city: str = Field(..., description="City name")
    state: None = None

meal_deduction_special_cases = ["russia", "armenia", "azerbaijan", "belarus", "estonia", "georgia", "kazakhstan", 
"kyrgyzstan", "latvia", "lithuania", "moldova", "tajikistan", "turkmenistan", "ukraine", "uzbekistan"]

class StayModel(BaseModel):
    days: int = Field(..., ge=1, description="Number of days for stipend")
    location: USLocation | ForeignLocation
    # Optional: flags for travel-day positions
    is_first_travel_day: bool = False
    is_last_travel_day: bool = False

class MealDeductionModel(BaseModel):
    deduct_meals: bool
    custom_daily_deduction: Optional[int] = None
class PerDiemRequest(BaseModel):
    stays: List[StayModel]

class StayCostModel(BaseModel):
    location: USLocation | ForeignLocation
    meal_cost_usd: float = Field(..., ge=0)
    lodging_cost_usd: float = Field(..., ge=0)
    total_cost_usd: float = Field(..., ge=0)
    # optional local currency echo
    local_currency: str
    local_amount: float

class PerDiemResponse(BaseModel):
    costs: list[StayCostModel]

# ---------- Constants ----------

INTL_OTHER = 80.0        # not used here per your scope exclusion
ETHIOPIA_FLAT = 25.0     # covers meals+incidentals+lodging
US_DAILY_CAP = 80.0

def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().strip().lower()

def _dssr_daily_usd(country: CountryCode, city: str) -> float:
    rows = fetch_dos_per_diem(country)
    city_norm = _norm(city)
    other_rate = 0
    best = 0
    for r in rows:
        post = _norm(r.post_name)
        if post == city_norm:
            best = max(best, r.max_per_diem_rate)
        if r.post_name == "Other":
            other_rate = r.max_per_diem_rate
    return best or other_rate or 0.0

def _philippines_tier_php(city: str) -> Tuple[int, str]:
    c = _norm(city)
    if c in {"manila", "metro manila", "ncr"}:
        return 2200, "PHP"
    if c in {"cebu", "cebu city", "davao", "davao city"}:
        return 1800, "PHP"
    return 1500, "PHP"

# ---------- Core daily calculation (stipend per day, no meal deductions) ----------

def _daily_stipend_usd_and_local(loc: USLocation | ForeignLocation) -> Tuple[float, str, float]:
    # United States: GSA M&IE with $80/day cap
    if loc.kind == "us":
        mie = fetch_gsa_mie(loc.city, loc.state, dt.date.today())
        return min(mie, US_DAILY_CAP), "USD", min(mie, US_DAILY_CAP)

    # Cameroon: XAF 40,000 (no deductions)
    if loc.country == CountryCode.CAMEROON:
        local_amt = 40000.0
        usd = convert_to_currency(local_amt, Currency.CENTRAL_AFRICAN_CFA, Currency.US_DOLLAR)
        return usd, "XAF", local_amt

    # Ethiopia: $25 flat covers meals+incidentals+lodging
    if loc.country == CountryCode.ETHIOPIA:
        return ETHIOPIA_FLAT, "USD", ETHIOPIA_FLAT

    # Philippines: 2200/1800/1500 PHP by city bucket
    if loc.country == CountryCode.PHILIPPINES:
        php, code = _philippines_tier_php(loc.city)
        usd = convert_to_currency(php, Currency.PHILIPPINE_PESO, Currency.US_DOLLAR)
        return usd, code, float(php)

    usd = _dssr_daily_usd(loc.country, loc.city)
    return usd, "USD", usd

# ---------- Public entrypoint ----------

def get_per_diem_estimate(request: PerDiemRequest) -> PerDiemResponse:
    costs: List[StayCostModel] = []
    for stay in request.stays:
        daily_usd, local_code, local_amt = _daily_stipend_usd_and_local(stay.location)

        # Apply 75% travel-day rule here if you choose to implement now:
        multiplier = 1.0
        if stay.is_first_travel_day or stay.is_last_travel_day:
            multiplier = 0.75

        stipend_usd_total = round(daily_usd * stay.days * multiplier, 2)

        # Ethiopia note: $25 covers lodging+meals; we keep lodging at 0 here but document
        meal_cost_usd = stipend_usd_total
        lodging_cost_usd = 0.0
        total_cost_usd = stipend_usd_total

        costs.append(
            StayCostModel(
                location=stay.location,
                meal_cost_usd=meal_cost_usd,
                lodging_cost_usd=lodging_cost_usd,
                total_cost_usd=total_cost_usd,
                local_currency=local_code,
                local_amount=(round(local_amt * stay.days * multiplier, 2)),
            )
        )
    return PerDiemResponse(costs=costs)