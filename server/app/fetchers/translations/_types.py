from enum import Enum
from typing import Dict, Literal, Optional

from pydantic import BaseModel

translation_type = Literal["Translation", "Interpretation", "Consecutive Interpretation", "Simultaneous Interpretation", "Editing"]

uom_time = Literal["Hour", "Day", "Half Day"]

uom_words = Literal["Word", "Rush Rate (Word)", "Overtime Hour", "Page"]

class LanguageName(str, Enum):
    AZERBAIJANI = "AZERBAIJANI"
    ENGLISH = "ENGLISH"
    SPANISH = "SPANISH"
    FRENCH = "FRENCH"
    PORTUGUESE = "PORTUGUESE"
    ITALIAN = "ITALIAN"
    GERMAN = "GERMAN"
    DUTCH = "DUTCH"
    CHINESE = "CHINESE"
    VIETNAMESE = "VIETNAMESE"
    HINDI = "HINDI"
    BENGALI = "BENGALI"
    POLISH = "POLISH"
    SWEDISH = "SWEDISH"

    ARABIC = "ARABIC"
    RUSSIAN = "RUSSIAN"
    UKRAINIAN = "UKRAINIAN"
    ROMANIAN = "ROMANIAN"
    TURKISH = "TURKISH"
    KOREAN = "KOREAN"
    JAPANESE = "JAPANESE"
    THAI = "THAI"
    GREEK = "GREEK"
    HEBREW = "HEBREW"
    PERSIAN = "PERSIAN"
    CZECH = "CZECH"
    SLOVAK = "SLOVAK"
    HUNGARIAN = "HUNGARIAN"
    LITHUANIAN = "LITHUANIAN"
    LATVIAN = "LATVIAN"
    ESTONIAN = "ESTONIAN"
    DANISH = "DANISH"
    NORWEGIAN = "NORWEGIAN"
    FINNISH = "FINNISH"
    MALAY = "MALAY"
    INDONESIAN = "INDONESIAN"
    TAGALOG = "TAGALOG"
    SERBIAN = "SERBIAN"
    CROATIAN = "CROATIAN"
    BOSNIAN = "BOSNIAN"
    BULGARIAN = "BULGARIAN"
    SLOVENIAN = "SLOVENIAN"
    ALBANIAN = "ALBANIAN"
    GEORGIAN = "GEORGIAN"
    ARMENIAN = "ARMENIAN"
    KUNG = "!KUNG"

    MONGOLIAN = "MONGOLIAN"
    LAO = "LAO"
    KHMER = "KHMER"
    AMHARIC = "AMHARIC"
    TIGRINYA = "TIGRINYA"
    SOMALI = "SOMALI"
    ZULU = "ZULU"
    XHOSA = "XHOSA"
    AFRIKAANS = "AFRIKAANS"
    SWAHILI = "SWAHILI"
    KINYARWANDA = "KINYARWANDA"
    KIRUNDI = "KIRUNDI"
    WOLOF = "WOLOF"
    HAUSA = "HAUSA"
    YORUBA = "YORUBA"
    IGBO = "IGBO"
    TWI = "TWI"
    LUXEMBOURGISH = "LUXEMBOURGISH"
    FAROESE = "FAROESE"
    ICELANDIC = "ICELANDIC"
    UZBEK = "UZBEK"
    TAJIK = "TAJIK"
    TURKMEN = "TURKMEN"
    KYRGYZ = "KYRGYZ"
    KAZAKH = "KAZAKH"
    PASHTO = "PASHTO"
    DARI = "DARI"
    NEPALI = "NEPALI"
    SINHALA = "SINHALA"
    TAMIL = "TAMIL"
    URDU = "URDU"
    MACEDONIAN = "MACEDONIAN"
    BASQUE = "BASQUE"
    CATALAN = "CATALAN"
    GALICIAN = "GALICIAN"
    BELARUSIAN = "BELARUSIAN"
    TONGAN = "TONGAN"
    SAMOAN = "SAMOAN"
    FIJIAN = "FIJIAN"
    BISLAMA = "BISLAMA"
    PALAUAN = "PALAUAN"
    MARSHALLESE = "MARSHALLESE"
    NAURUAN = "NAURUAN"
    NIUEAN = "NIUEAN"
    TOKELAUAN = "TOKELAUAN"
    GREENLANDIC = "GREENLANDIC"
    TAHITIAN = "TAHITIAN"
    REUNION_FRENCH = "REUNION_FRENCH"
    MAYOTTE_FRENCH = "MAYOTTE_FRENCH"

BandLiteral = Literal["tier1", "tier2", "tier3", "tier4"]

# Industry-aligned rates (freelancer base rates)
BASE_RATES = {
    "tier1": {
        "translation": {"min": 0.10, "max": 0.15},
        "consecutive_interpretation": {"min": 50, "max": 120},
        "simultaneous_interpretation": {"min": 70, "max": 150}
    },
    "tier2": {
        "translation": {"min": 0.15, "max": 0.20},
        "consecutive_interpretation": {"min": 70, "max": 150},
        "simultaneous_interpretation": {"min": 90, "max": 180}
    },
    "tier3": {
        "translation": {"min": 0.20, "max": 0.30},
        "consecutive_interpretation": {"min": 90, "max": 180},
        "simultaneous_interpretation": {"min": 110, "max": 220}
    },
    "tier4": {
        "translation": {"min": 0.25, "max": 0.40},
        "consecutive_interpretation": {"min": 110, "max": 200},
        "simultaneous_interpretation": {"min": 130, "max": 250}
    }
}

# Country-based rate multipliers (relative to US baseline)
COUNTRY_MULTIPLIERS = {
    "US": 1.0,
    "CHINA": 0.6,
    "JAPAN": 0.9,
    "GERMANY": 0.8,
    "FRANCE": 0.8,
    "UK": 0.7,
    "CANADA": 0.85,
    "SPAIN": 0.7,
    "ITALY": 0.7,
    "NETHERLANDS": 0.8,
    "SWEDEN": 0.9,
    "SWITZERLAND": 1.1,
    "BRAZIL": 0.65,
    "INDIA": 0.45,
    "SOUTH_KOREA": 0.8,
    "AUSTRALIA": 0.85,
    "RUSSIA": 0.65,
    "MEXICO": 0.65,
    "ARGENTINA": 0.55,
    "TURKEY": 0.65,
    "POLAND": 0.7,
    "DEFAULT": 0.8
}

UOM_MAP = {
    # Words
    "target word": "Word",
    "source word": "Word",
    "word": "Word",
    "source wrd": "Word",
    "target wrd": "Word",
    "english word": "Word",
    "slides": "Page",
    "page": "Page",
    "drawing": "Page",
    "rush rate (word)": "Rush Rate (Word)",
    "rush rate": "Rush Rate (Word)",
    "overtime hour": "Overtime Hour",

    # Time
    "hour": "Hour",
    "minute": "Hour",           # normalize to Hour granularity
    "day": "Day",
    "8-hr day": "Day",
    "8-hr. day": "Day",
    "10-hr. day": "Day",
    "4-hr half day": "Half Day",
    "half day": "Half Day",

    # Ambiguous or ignored → can drop or map separately
    "flat rate": None,
    "each": None,
    "project": None,
    "package": None,
    "minimum fee": None,
    "null": None,
}

# Industry-aligned 4-tier language classification
LANGUAGE_BANDS: Dict[LanguageName, BandLiteral] = {
    # Tier 1: Common languages (Spanish, French, German, Italian, Portuguese)
    LanguageName.ENGLISH: "tier1",
    LanguageName.SPANISH: "tier1",
    LanguageName.FRENCH: "tier1",
    LanguageName.PORTUGUESE: "tier1",
    LanguageName.ITALIAN: "tier1",
    LanguageName.GERMAN: "tier1",
    LanguageName.REUNION_FRENCH: "tier1",
    LanguageName.MAYOTTE_FRENCH: "tier1",

    # Tier 2: Mid-demand languages (Dutch, Polish, Russian, Turkish, Swedish)
    LanguageName.DUTCH: "tier2",
    LanguageName.POLISH: "tier2",
    LanguageName.RUSSIAN: "tier2",
    LanguageName.TURKISH: "tier2",
    LanguageName.SWEDISH: "tier2",
    LanguageName.UKRAINIAN: "tier2",
    LanguageName.ROMANIAN: "tier2",
    LanguageName.CZECH: "tier2",
    LanguageName.SLOVAK: "tier2",
    LanguageName.HUNGARIAN: "tier2",
    LanguageName.DANISH: "tier2",
    LanguageName.NORWEGIAN: "tier2",
    LanguageName.FINNISH: "tier2",
    LanguageName.GREEK: "tier2",
    LanguageName.SERBIAN: "tier2",
    LanguageName.CROATIAN: "tier2",
    LanguageName.BOSNIAN: "tier2",
    LanguageName.BULGARIAN: "tier2",
    LanguageName.SLOVENIAN: "tier2",
    LanguageName.ALBANIAN: "tier2",
    LanguageName.LITHUANIAN: "tier2",
    LanguageName.LATVIAN: "tier2",
    LanguageName.ESTONIAN: "tier2",

    # Tier 3: Asian/Middle Eastern languages (Chinese, Japanese, Korean, Arabic, Hindi)
    LanguageName.CHINESE: "tier3",
    LanguageName.JAPANESE: "tier3",
    LanguageName.KOREAN: "tier3",
    LanguageName.ARABIC: "tier3",
    LanguageName.HINDI: "tier3",
    LanguageName.HEBREW: "tier3",
    LanguageName.PERSIAN: "tier3",
    LanguageName.THAI: "tier3",
    LanguageName.MALAY: "tier3",
    LanguageName.INDONESIAN: "tier3",
    LanguageName.GEORGIAN: "tier3",
    LanguageName.ARMENIAN: "tier3",

    # Tier 4: Rare/Regional languages (Vietnamese, Bengali, Tamil, Urdu, Finnish, Estonian)
    LanguageName.VIETNAMESE: "tier4",
    LanguageName.BENGALI: "tier4",
    LanguageName.TAMIL: "tier4",
    LanguageName.URDU: "tier4",
    LanguageName.TAGALOG: "tier4",
    LanguageName.AZERBAIJANI: "tier4",
    LanguageName.MONGOLIAN: "tier4",
    LanguageName.LAO: "tier4",
    LanguageName.KHMER: "tier4",
    LanguageName.AMHARIC: "tier4",
    LanguageName.TIGRINYA: "tier4",
    LanguageName.SOMALI: "tier4",
    LanguageName.ZULU: "tier4",
    LanguageName.XHOSA: "tier4",
    LanguageName.AFRIKAANS: "tier4",
    LanguageName.SWAHILI: "tier4",
    LanguageName.KINYARWANDA: "tier4",
    LanguageName.KIRUNDI: "tier4",
    LanguageName.WOLOF: "tier4",
    LanguageName.HAUSA: "tier4",
    LanguageName.YORUBA: "tier4",
    LanguageName.IGBO: "tier4",
    LanguageName.TWI: "tier4",
    LanguageName.LUXEMBOURGISH: "tier4",
    LanguageName.FAROESE: "tier4",
    LanguageName.ICELANDIC: "tier4",
    LanguageName.UZBEK: "tier4",
    LanguageName.TAJIK: "tier4",
    LanguageName.TURKMEN: "tier4",
    LanguageName.KYRGYZ: "tier4",
    LanguageName.KAZAKH: "tier4",
    LanguageName.PASHTO: "tier4",
    LanguageName.DARI: "tier4",
    LanguageName.NEPALI: "tier4",
    LanguageName.SINHALA: "tier4",
    LanguageName.MACEDONIAN: "tier4",
    LanguageName.BASQUE: "tier4",
    LanguageName.CATALAN: "tier4",
    LanguageName.GALICIAN: "tier4",
    LanguageName.BELARUSIAN: "tier4",
    LanguageName.TONGAN: "tier4",
    LanguageName.SAMOAN: "tier4",
    LanguageName.FIJIAN: "tier4",
    LanguageName.BISLAMA: "tier4",
    LanguageName.PALAUAN: "tier4",
    LanguageName.MARSHALLESE: "tier4",
    LanguageName.NAURUAN: "tier4",
    LanguageName.NIUEAN: "tier4",
    LanguageName.TOKELAUAN: "tier4",
    LanguageName.GREENLANDIC: "tier4",
    LanguageName.TAHITIAN: "tier4"
}

UOM = uom_words | uom_time

def parse_uom(raw: str) -> UOM | None:
    """Normalize raw UoM string to canonical Literal or None if not applicable"""
    if not raw:
        return None
    key = raw.strip().lower()
    return UOM_MAP.get(key, None)


class HistoricalData(BaseModel):
    category: translation_type
    service: str
    translator_us_citizen: Optional[str] = None
    country: str
    uom: str
    src: LanguageName
    target: LanguageName
    translation_direction: Literal["To", "To / From"]
    vendor_rate: float

class TranslationModel(BaseModel):
    src: LanguageName
    target: LanguageName
    type: Literal["Translation"]
    uom: uom_words
    quantity: int
    country: Optional[str] = "US"  # Default to US pricing
    provider_type: Literal["freelancer", "agency"] = "freelancer"
    urgency: Literal["standard", "rush"] = "standard"
    volume_discount: bool = False  # For large projects (>5000 words)

class InterpretationModel(BaseModel):
    src: LanguageName
    target: LanguageName
    type: Literal["Interpretation", "Consecutive Interpretation", "Simultaneous Interpretation"]
    uom: uom_time
    quantity: int
    country: Optional[str] = "US"  # Default to US pricing
    provider_type: Literal["freelancer", "agency"] = "freelancer"
    urgency: Literal["standard", "rush"] = "standard"


class TranslationRequest(BaseModel):
    jobs: list[TranslationModel | InterpretationModel]

class EstimateModel(BaseModel):
    total: float
    # Default to formula if we have historical data, else-wise use napkin math
    explaination: str

class TranslationResponse(BaseModel):
    estimates: list[EstimateModel]