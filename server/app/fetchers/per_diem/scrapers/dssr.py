from __future__ import annotations
import re
import datetime as dt
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Optional
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from app.fetchers.per_diem._types import CountryCode

# --- Structured row ---
@dataclass
class PerDiemRow:
    country_name: str
    post_name: str
    season_begin: str
    season_end: str
    max_lodging_rate: int
    mie_rate: int
    max_per_diem_rate: int
    footnote_numbers: Optional[List[int]]
    footnote_url: Optional[str]
    effective_date: dt.date

# --- Constants ---
BASE = "https://allowances.state.gov/web920"
FORM_URL = f"{BASE}/per_diem.asp"
ACTION_URL = f"{BASE}/per_diem_action.asp"
FOOT_NOTE_BASE = f"{BASE}/"

EXPECTED_HEADERS = [
    "country name",
    "post name",
    "season begin",
    "season end",
    "maximum lodging rate",
    "m and ie rate",            # normalize "M & IE Rate"
    "maximum per diem rate",
    "footnote",
    "effective date",
]
EFFECTIVE_DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")

FOOTNOTE_RE: re.Pattern[str] = re.compile(r"Footnote=([\d,]+)", re.IGNORECASE)

# --- Utils ---
def _norm(text: str) -> str:
    t = (text or "").replace("\xa0", " ").strip()
    return re.sub(r"\s+", " ", t)

def _header_key(text: str) -> str:
    t = _norm(text).lower().replace("&", "and")
    return re.sub(r"\s+", " ", t)

def _to_int(s: str) -> int:
    s2 = re.sub(r"[^\d]", "", s or "")
    return int(s2) if s2 else 0

def _iter_tags(nodes: Iterable[object]) -> Iterator[Tag]:
    for n in nodes:
        if isinstance(n, Tag):
            yield n

def _first_tag(node: object | None, name: str) -> Optional[Tag]:
    if isinstance(node, Tag):
        # find returns Optional[Tag]
        return node.find(name)  # type: ignore[no-any-return]  # bs4 stubs can be imprecise
    return None

def _find_all_tags(node: object | None, name: str) -> List[Tag]:
    if isinstance(node, Tag):
        return list(_iter_tags(node.find_all(name)))
    return []

def _is_real_results_table(tbl: Tag) -> bool:
    head_tr = _first_tag(tbl, "tr")
    if head_tr is None:
        return False
    ths = _find_all_tags(head_tr, "th")
    if len(ths) != 9:
        return False
    headers = [_header_key(th.get_text()) for th in ths]
    return headers == EXPECTED_HEADERS

def _get_href_str(tag: Optional["Tag"]) -> Optional[str]:
    """Return tag['href'] as a str if present and is a string; else None."""
    if tag is None:
        return None
    href = tag.attrs.get("href")
    return href if isinstance(href, str) else None

# --- Parser ---
def parse_per_diem_table(html: str) -> List[PerDiemRow]:
    soup = BeautifulSoup(html, "html.parser")

    # Choose the table whose headers exactly match the expected 9 columns
    tables = _find_all_tags(soup, "table")
    table: Optional[Tag] = next((t for t in tables if _is_real_results_table(t)), None)
    if table is None:
        return []

    rows: List[PerDiemRow] = []
    trs = _find_all_tags(table, "tr")
    for tr in trs[1:]:  # skip header
        tds = _find_all_tags(tr, "td")
        if len(tds) != 9:
            continue

        vals = [_norm(td.get_text(" ", strip=True)) for td in tds]
        (country_name, post_name, season_begin, season_end,
         max_lodging_raw, mie_raw, max_pd_raw, _foot_td_txt, eff_raw) = vals

        # Filter any stray nav rows (defensive)
        cn_lower = country_name.lower()
        if "allowances by" in cn_lower or "previous rates" in cn_lower:
            continue

        # Require full MM/DD/YYYY to avoid ambiguous parsing
        if not EFFECTIVE_DATE_RE.match(eff_raw):
            continue
        effective_date = dt.datetime.strptime(eff_raw, "%m/%d/%Y").date()

        # Footnote link (optional)
        foot_a = _first_tag(tds[7], "a")
        foot_url_rel: Optional[str] = _get_href_str(foot_a)

        foot_url_abs: Optional[str] = None
        foot_nums: Optional[List[int]] = None

        if isinstance(foot_url_rel, str):
            foot_url_abs = FOOT_NOTE_BASE + foot_url_rel.lstrip("/")
            m = FOOTNOTE_RE.search(foot_url_rel)  # <-- str arg, typed pattern
            if m:
                foot_nums = [int(x) for x in m.group(1).split(",") if x.isdigit()]

        rows.append(
            PerDiemRow(
                country_name=country_name,
                post_name=post_name,
                season_begin=season_begin,
                season_end=season_end,
                max_lodging_rate=_to_int(max_lodging_raw),
                mie_rate=_to_int(mie_raw),
                max_per_diem_rate=_to_int(max_pd_raw),
                footnote_numbers=foot_nums,
                footnote_url=foot_url_abs,
                effective_date=effective_date,
            )
        )
    return rows

# --- Fetch + parse ---
def fetch_dos_per_diem(country: CountryCode, post_query: str = "") -> List[PerDiemRow]:
    s = requests.Session()
    s.get(FORM_URL, timeout=15)  # prime cookies
    payload = {"CountryCode": country.value, "Post": post_query}
    res = s.post(ACTION_URL, data=payload, timeout=20)
    res.raise_for_status()
    return parse_per_diem_table(res.text)