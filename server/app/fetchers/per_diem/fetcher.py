from __future__ import annotations
from typing import List, Literal, Optional, Tuple
from pydantic import BaseModel, Field
import unicodedata
import datetime as dt

from app.fetchers.per_diem._types import (
    COUNTRY_TO_CURRENCY,
    CountryCode,
    CountryName,
    USStateCode,
    country_name_to_code_enum,
)
from app.fetchers.per_diem.scrapers.dssr import PerDiemRow, fetch_dos_per_diem
from app.fetchers.per_diem.scrapers.exchange_rate import Currency, convert_to_currency
from app.fetchers.per_diem.scrapers.gsa import fetch_gsa_data

# ---------- Models ----------


class USLocation(BaseModel):
    kind: Literal["us"] = "us"
    country: CountryName
    state: USStateCode
    city: str = Field(..., description="City name")


class ForeignLocation(BaseModel):
    kind: Literal["foreign"] = "foreign"
    country: CountryName
    city: str = Field(..., description="City name")
    state: None = None


meal_deduction_special_cases = [
    CountryCode.RUSSIA,
    CountryCode.ARMENIA,
    CountryCode.AZERBAIJAN,
    CountryCode.BELARUS,
    CountryCode.ESTONIA,
    CountryCode.GEORGIA,
    CountryCode.KAZAKHSTAN,
    CountryCode.KYRGYZSTAN,
    CountryCode.LATVIA,
    CountryCode.LITHUANIA,
    CountryCode.MOLDOVA,
    CountryCode.TAJIKISTAN,
    CountryCode.TURKMENISTAN,
    CountryCode.UKRAINE,
    CountryCode.UZBEKISTAN,
]


class StayModel(BaseModel):
    days: int = Field(..., ge=1, description="Number of days for stipend")
    location: USLocation | ForeignLocation
    # Optional: flags for travel-day positions
    is_first_travel_day: bool = False
    is_last_travel_day: bool = False
    deduct_meals: bool


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

INTL_OTHER = 80.0  # not used here per your scope exclusion
ETHIOPIA_FLAT = 25.0  # covers meals+incidentals+lodging
US_DAILY_CAP = 80.0


def _norm(s: str) -> str:
    return (
        unicodedata.normalize("NFKD", s or "")
        .encode("ascii", "ignore")
        .decode()
        .strip()
        .lower()
    )


def _dssr_foreign_per_diem(country: CountryCode, city: str) -> PerDiemRow:
    rows = fetch_dos_per_diem(country)
    city_norm = _norm(city)
    row_index = -1
    other_index = -1
    for i, r in enumerate(rows):
        post = _norm(r.post_name)
        if post == city_norm:
            row_index = i
            break
        if r.post_name == "Other":
            other_index = i

    return rows[row_index if row_index != -1 else other_index]


def _philippines_tier_php(city: str) -> Tuple[int, str]:
    """
    Determine the PHP tier for a given city in the Philippines.
    returns (amount, currency)
    """

    c = _norm(city)
    if c in {"manila", "metro manila", "ncr"}:
        return 2200, Currency.PHILIPPINE_PESO.value
    if c in {"cebu", "cebu city", "davao", "davao city"}:
        return 1800, Currency.PHILIPPINE_PESO.value
    return 1500, Currency.PHILIPPINE_PESO.value


# ---------- Core daily calculation (stipend per day, no meal deductions) ----------


def _daily_stipend_usd_and_local(
    loc: USLocation | ForeignLocation, meal_deductions: bool
) -> Tuple[float, str, float, float, float]:
    """

    Fetch from GSA or DSSR the cost that it will take for a person to stay in a location lodging
    and M&IE wise.

    Returns:
        (cost_usd, local_currency, cost_local_currency, lodging_usd, lodging_local_currency)

    """

    # United States: GSA M&IE with $80/day cap
    if loc.kind == "us":
        mie, lodging = fetch_gsa_data(loc.city, loc.state, dt.date.today())
        daily = min(mie, US_DAILY_CAP)

        if meal_deductions:
            daily = daily * 0.2

        return daily, "USD", daily, lodging, lodging

    (
        cost_usd,
        local_currency,
        cost_local_currency,
        lodging_usd,
        lodging_local_currency,
    ) = 0, "", 0, 0, 0

    country_code = country_name_to_code_enum(loc.country)

    # Cameroon: XAF 40,000 (no deductions)
    if country_code == CountryCode.CAMEROON:
        cost_local_currency = 40000.0
        cost_usd = convert_to_currency(
            cost_local_currency, Currency.CENTRAL_AFRICAN_CFA, Currency.US_DOLLAR
        )
        local_currency = Currency.CENTRAL_AFRICAN_CFA.value

    # Ethiopia: $25 flat covers meals+incidentals+lodging
    if country_code == CountryCode.ETHIOPIA:
        cost_usd = ETHIOPIA_FLAT
        cost_local_currency = convert_to_currency(
            ETHIOPIA_FLAT, Currency.US_DOLLAR, Currency.ETHIOPIAN_BIRR
        )
        local_currency = Currency.ETHIOPIAN_BIRR.value
        lodging_usd = 0.0
        lodging_local_currency = 0.0
        # We escape here as the $25 covers everything
        return (
            cost_usd,
            local_currency,
            cost_local_currency,
            lodging_usd,
            lodging_local_currency,
        )

    # Philippines: 2200/1800/1500 PHP by city bucket
    if country_code == CountryCode.PHILIPPINES:
        php, code = _philippines_tier_php(loc.city)
        cost_usd = convert_to_currency(
            php, Currency.PHILIPPINE_PESO, Currency.US_DOLLAR
        )
        cost_local_currency = php
        local_currency = code

    row = _dssr_foreign_per_diem(country_code, loc.city)

    if local_currency == "":
        # We have no data, use row for all fields
        lodging_usd = row.max_lodging_rate
        local_currency = COUNTRY_TO_CURRENCY[country_code].value
        cost_usd = row.mie_rate
        cost_local_currency = convert_to_currency(
            cost_usd, Currency.US_DOLLAR, COUNTRY_TO_CURRENCY[country_code]
        )
        lodging_local_currency = convert_to_currency(
            lodging_usd, Currency.US_DOLLAR, COUNTRY_TO_CURRENCY[country_code]
        )

    else:
        # We have partially complete data, fill out the rest for lodging
        lodging_usd = row.max_lodging_rate
        lodging_local_currency = convert_to_currency(
            lodging_usd, Currency.US_DOLLAR, COUNTRY_TO_CURRENCY[country_code]
        )

    if meal_deductions:
        if country_code in meal_deduction_special_cases:
            cost_usd = cost_usd - 35
        else:
            cost_usd = cost_usd * 0.2

        cost_local_currency = convert_to_currency(
            cost_usd, Currency.US_DOLLAR, COUNTRY_TO_CURRENCY[country_code]
        )

    return (
        cost_usd,
        local_currency,
        cost_local_currency,
        lodging_usd,
        lodging_local_currency,
    )


# ---------- Public entrypoint ----------


def get_per_diem_estimate(request: PerDiemRequest) -> PerDiemResponse:
    costs: List[StayCostModel] = []
    for stay in request.stays:
        mie_usd, local_code, mie_local, lodging_usd, lodging_local_amt = (
            _daily_stipend_usd_and_local(stay.location, stay.deduct_meals)
        )

        meal_cost_usd = mie_usd * stay.days
        lodging_cost_usd = lodging_usd * stay.days

        local_total = round(mie_local * stay.days, 2) + round(
            lodging_local_amt * stay.days, 2
        )

        costs.append(
            StayCostModel(
                location=stay.location,
                meal_cost_usd=meal_cost_usd,
                lodging_cost_usd=lodging_cost_usd,
                total_cost_usd=meal_cost_usd + lodging_cost_usd,
                local_currency=local_code,
                local_amount=local_total,
            )
        )
    return PerDiemResponse(costs=costs)
