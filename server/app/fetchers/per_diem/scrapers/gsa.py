from typing import Optional
import datetime as dt
import requests


US_MIE_CAP = 80.0

def fetch_gsa_mie(city: Optional[str], state: Optional[str], when: Optional[dt.date] = None,
                   api_key: Optional[str] = None) -> float:
    """
    Fetch US M&IE via GSA API; cap at $80/day. Falls back to cap if not found.
    Docs: https://open.gsa.gov/api/perdiem/
    """
    if not state:
        return US_MIE_CAP

    when = when or dt.date.today()
    year, month = when.year, when.month
    url = "https://api.gsa.gov/travel/perdiem/v2/rates/city/state/monthyear"
    params = {"city": (city or "").title(), "state": state.upper(), "monthyear": f"{month:02d}{year}"}
    headers = {"X-Api-Key": api_key} if api_key else {}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        rates = data.get("rates", [])
        if rates:
            mie = rates[0].get("mie")
            if mie is not None:
                val = float(str(mie).replace("$", "").strip())
                return min(val, US_MIE_CAP)
    except Exception:
        pass

    return US_MIE_CAP