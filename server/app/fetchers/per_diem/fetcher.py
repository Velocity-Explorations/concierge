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

# Countries that should use DSSR M&IE rates with meal deductions per contract
dssr_countries = [
    CountryCode.KENYA,
    CountryCode.TANZANIA,
    CountryCode.NIGERIA,
    CountryCode.MALAYSIA,
    CountryCode.VIETNAM,
]


class StayModel(BaseModel):
    days: int = Field(..., ge=1, description="Number of days for stipend")
    location: USLocation | ForeignLocation
    # Travel day flags - by default first and last days are travel days
    is_first_travel_day: bool = True
    is_last_travel_day: bool = True
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
    # Breakdown for transparency
    meal_breakdown: str = ""
    daily_mie_rate: float = 0.0
    travel_day_adjustment: str = ""


class PerDiemResponse(BaseModel):
    costs: list[StayCostModel]


# ---------- Constants ----------

INTL_OTHER = 80.0
ETHIOPIA_FLAT = 25.0  # covers meals+incidentals+lodging
US_DAILY_CAP = 80.0
INTERNATIONAL_DAILY_RATE = 80.0
DOMESTIC_DAILY_RATE = 40.0
RUSSIA_CIS_INTL_RATE = 40.0


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


def _is_domestic_travel(request: PerDiemRequest) -> bool:
    """
    Check if all stays are in the same country (domestic travel).
    """
    countries = set()
    for stay in request.stays:
        if stay.location.kind == "us":
            countries.add("US")
        else:
            countries.add(stay.location.country)
    
    return len(countries) == 1


def _calculate_travel_days_total(daily_rate: float, stay: StayModel) -> Tuple[float, str]:
    """
    Calculate total cost applying 75% for travel days.
    Returns (total, breakdown_text)
    """
    total = 0.0
    breakdown_parts = []
    travel_days_count = 0
    full_days_count = 0
    
    for day in range(stay.days):
        day_rate = daily_rate
        # Apply 75% rate for first and last travel days
        if (day == 0 and stay.is_first_travel_day) or \
           (day == stay.days - 1 and stay.is_last_travel_day and stay.days > 1):
            day_rate = daily_rate * 0.75
            travel_days_count += 1
        else:
            full_days_count += 1
        total += day_rate
    
    # Build breakdown text
    if travel_days_count > 0:
        travel_total = daily_rate * 0.75 * travel_days_count
        breakdown_parts.append(f"{travel_days_count} travel day{'s' if travel_days_count > 1 else ''} @ 75% rate (${daily_rate:.2f} × 0.75 × {travel_days_count} = ${travel_total:.2f})")
    if full_days_count > 0:
        full_total = daily_rate * full_days_count
        breakdown_parts.append(f"{full_days_count} full day{'s' if full_days_count > 1 else ''} @ 100% rate (${daily_rate:.2f} × {full_days_count} = ${full_total:.2f})")
    
    breakdown = "; ".join(breakdown_parts) if breakdown_parts else "No days calculated"
    return round(total, 2), breakdown


# ---------- Core daily calculation (stipend per day, no meal deductions) ----------


def _daily_stipend_usd_and_local(
    loc: USLocation | ForeignLocation,
    meal_deductions: bool,
    is_domestic: bool = False
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

    # Foreign locations - simplified logic
    country_code = country_name_to_code_enum(loc.country)
    cost_usd = 0.0
    lodging_usd = 0.0
    local_currency = COUNTRY_TO_CURRENCY[country_code].value
    
    # Specific country rates
    if country_code == CountryCode.CAMEROON:
        cost_usd = convert_to_currency(40000.0, Currency.CENTRAL_AFRICAN_CFA, Currency.US_DOLLAR)
        local_currency = Currency.CENTRAL_AFRICAN_CFA.value

    elif country_code == CountryCode.ETHIOPIA:
        cost_usd = ETHIOPIA_FLAT
        local_currency = Currency.ETHIOPIAN_BIRR.value
        # Ethiopia: $25 flat rate with NO meal deductions per contract
        cost_local_currency = convert_to_currency(cost_usd, Currency.US_DOLLAR, Currency.ETHIOPIAN_BIRR)
        return cost_usd, local_currency, cost_local_currency, 0.0, 0.0
    
    elif country_code == CountryCode.PHILIPPINES:
        php, code = _philippines_tier_php(loc.city)
        cost_usd = convert_to_currency(php, Currency.PHILIPPINE_PESO, Currency.US_DOLLAR)
        local_currency = code
        # Philippines uses Double Payment Policy (EO 77) - handle separately
        if meal_deductions:
            # EO 77 deductions are applied in local currency (PHP) then converted
            deducted_php = php * 0.2  # 80% total deduction per contract
            cost_usd = convert_to_currency(deducted_php, Currency.PHILIPPINE_PESO, Currency.US_DOLLAR)

    elif is_domestic:
        cost_usd = DOMESTIC_DAILY_RATE

    elif country_code in dssr_countries:
        # Use DSSR M&IE rates for Kenya, Tanzania, Nigeria, Malaysia, Vietnam
        row = _dssr_foreign_per_diem(country_code, loc.city)
        cost_usd = row.mie_rate
        lodging_usd = row.max_lodging_rate
    elif country_code in meal_deduction_special_cases:
        cost_usd = RUSSIA_CIS_INTL_RATE
    else:
        cost_usd = INTERNATIONAL_DAILY_RATE
    
    # Get DSSR lodging for non-travel-category rates (if not already set)
    if lodging_usd == 0 and cost_usd not in [DOMESTIC_DAILY_RATE, RUSSIA_CIS_INTL_RATE, INTERNATIONAL_DAILY_RATE]:
        if country_code not in dssr_countries:  # Don't double-fetch for DSSR countries
            row = _dssr_foreign_per_diem(country_code, loc.city)
            lodging_usd = row.max_lodging_rate
    
    # Validate rates don't exceed DSSR/GSA maximums per contract
    if country_code not in [CountryCode.CAMEROON, CountryCode.ETHIOPIA, CountryCode.PHILIPPINES] and not is_domestic:
        row = _dssr_foreign_per_diem(country_code, loc.city)
        if cost_usd > row.mie_rate:
            cost_usd = row.mie_rate  # Cap at DSSR maximum
    
    # Apply meal deductions (Philippines already handled above, Cameroon and Ethiopia have no deductions per contract)
    if meal_deductions and country_code not in [CountryCode.PHILIPPINES, CountryCode.CAMEROON, CountryCode.ETHIOPIA]:
        if country_code in meal_deduction_special_cases:
            cost_usd = cost_usd - 35  # $8+$12+$15 = $35 total
        else:
            cost_usd = cost_usd * 0.2  # 20% remaining after 80% deduction
    
    # Calculate local currency amounts
    cost_local_currency = convert_to_currency(
        cost_usd, Currency.US_DOLLAR, COUNTRY_TO_CURRENCY.get(country_code, Currency.US_DOLLAR)
    )
    lodging_local_currency = convert_to_currency(
        lodging_usd, Currency.US_DOLLAR, COUNTRY_TO_CURRENCY.get(country_code, Currency.US_DOLLAR)
    )
    
    return cost_usd, local_currency, cost_local_currency, lodging_usd, lodging_local_currency


# ---------- Public entrypoint ----------


def get_per_diem_estimate(request: PerDiemRequest) -> PerDiemResponse:
    costs: List[StayCostModel] = []
    is_domestic = _is_domestic_travel(request)
    
    for stay in request.stays:
        daily_mie, local_code, mie_local, daily_lodging, lodging_local = (
            _daily_stipend_usd_and_local(stay.location, stay.deduct_meals, is_domestic)
        )

        # Calculate totals with 75% travel day rates and get breakdown
        total_meal_cost, meal_breakdown = _calculate_travel_days_total(daily_mie, stay)
        total_lodging_cost = daily_lodging * stay.days
        
        # Build travel day adjustment text
        travel_adjustment = ""
        if stay.is_first_travel_day or stay.is_last_travel_day:
            travel_adjustment = "GSA per diem rules apply 75% M&IE rate for first and last travel days"
        
        # Calculate local currency total proportionally
        if daily_mie > 0:
            local_meal_total = (total_meal_cost / (daily_mie * stay.days)) * (mie_local * stay.days) if stay.days > 0 else 0.0
        else:
            local_meal_total = 0.0
            
        local_total = round(local_meal_total + (lodging_local * stay.days), 2)

        costs.append(
            StayCostModel(
                location=stay.location,
                meal_cost_usd=round(total_meal_cost, 2),
                lodging_cost_usd=round(total_lodging_cost, 2),
                total_cost_usd=round(total_meal_cost + total_lodging_cost, 2),
                local_currency=local_code,
                local_amount=local_total,
                meal_breakdown=meal_breakdown,
                daily_mie_rate=daily_mie,
                travel_day_adjustment=travel_adjustment,
            )
        )
    return PerDiemResponse(costs=costs)
