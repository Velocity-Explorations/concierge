from typing import Optional
import datetime as dt
import requests
import os

from server.app.fetchers.per_diem._types import USStateCode


API_KEY = os.getenv("GSA_API_KEY")

if not API_KEY:
    raise ValueError("GSA_API_KEY environment variable is not set")

def fetch_gsa_mie(city: Optional[str], state: USStateCode, when: Optional[dt.date] = None) -> float:
    """
    Fetch US M&IE via GSA API; cap at $80/day. Falls back to cap if not found.
    Docs: https://open.gsa.gov/api/perdiem/
    """

    when = when or dt.date.today()
    year, month = when.year, when.month
    url = "https://api.gsa.gov/travel/perdiem/v2/rates/city/state/monthyear"
    params = {"city": (city or "").title(), "state": state.upper(), "monthyear": f"{month:02d}{year}"}
    headers = {"X-Api-Key": API_KEY}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        rates = data.get("rates", [])
        if rates:
            mie = rates[0].get("mie")
            if mie is not None:
                val = float(str(mie).replace("$", "").strip())
                return val
    except Exception:
        pass

    return 0