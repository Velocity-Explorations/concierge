from typing import Optional
import datetime as dt
import requests
import os

from app.fetchers.per_diem._types import USStateCode

from typing import List, Optional
from pydantic import BaseModel


class Month(BaseModel):
    value: int
    number: int
    short: str
    long: str


class Months(BaseModel):
    month: List[Month]


class RateDetail(BaseModel):
    months: Months
    meals: int
    zip: Optional[str]
    county: str
    city: str
    standardRate: str   # could be bool if you want to parse "false"/"true" → bool


class RateEntry(BaseModel):
    oconusInfo: Optional[str]
    rate: List[RateDetail]
    state: str
    year: int
    isOconus: str  # same note: could map to bool if desired


class GsaModel(BaseModel):
    request: Optional[str]
    errors: Optional[str]
    rates: List[RateEntry]
    version: Optional[str]

API_KEY = os.getenv("GSA_API_KEY")

if not API_KEY:
    raise ValueError("GSA_API_KEY environment variable is not set")

def fetch_gsa_data(city: Optional[str], state: USStateCode, when: Optional[dt.date] = None) -> tuple[int, int]:
    """
    Fetch US M&IE via GSA API; Returns, (M&IE total, lodging)
    Docs: https://open.gsa.gov/api/perdiem/
    """

    when = when or dt.date.today()
    year, month = when.year, when.month
    url = f"https://api.gsa.gov/travel/perdiem/v2/rates/city/{city}/state/{state.value}/year/{year}?api_key={API_KEY}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        validated_data = GsaModel.model_validate(data)

        if not validated_data.rates or not validated_data.rates[0].rate:
            raise ValueError("No valid rate found")

        mie_total = validated_data.rates[0].rate[0].meals
        lodging = validated_data.rates[0].rate[0].months.month[month - 1].value

        return mie_total, lodging

    except Exception:
        print("Error fetching GSA data")

    return 0, 0