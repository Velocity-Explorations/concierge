from enum import Enum
from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field

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

BandLiteral = Literal["common", "medium", "rare"]

NAPKIN_MATH_RATES = {
    "common": {"translation": 0.12, "interpretation_hour": 45.0},
    "medium": {"translation": 0.18, "interpretation_hour": 65.0}, 
    "rare": {"translation": 0.25, "interpretation_hour": 85.0}
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

LANGUAGE_BANDS: Dict[LanguageName, BandLiteral] = {
    LanguageName.ENGLISH: "common",
    LanguageName.SPANISH: "common",
    LanguageName.FRENCH: "common",
    LanguageName.PORTUGUESE: "common",
    LanguageName.ITALIAN: "common",
    LanguageName.GERMAN: "common",
    LanguageName.DUTCH: "common",
    LanguageName.CHINESE: "common",
    LanguageName.VIETNAMESE: "common",
    LanguageName.HINDI: "common",
    LanguageName.BENGALI: "common",
    LanguageName.POLISH: "common",
    LanguageName.SWEDISH: "common",

    LanguageName.ARABIC: "medium",
    LanguageName.RUSSIAN: "medium",
    LanguageName.UKRAINIAN: "medium",
    LanguageName.ROMANIAN: "medium",
    LanguageName.TURKISH: "medium",
    LanguageName.KOREAN: "medium",
    LanguageName.JAPANESE: "medium",
    LanguageName.THAI: "medium",
    LanguageName.GREEK: "medium",
    LanguageName.HEBREW: "medium",
    LanguageName.PERSIAN: "medium",
    LanguageName.CZECH: "medium",
    LanguageName.SLOVAK: "medium",
    LanguageName.HUNGARIAN: "medium",
    LanguageName.LITHUANIAN: "medium",
    LanguageName.LATVIAN: "medium",
    LanguageName.ESTONIAN: "medium",
    LanguageName.DANISH: "medium",
    LanguageName.NORWEGIAN: "medium",
    LanguageName.FINNISH: "medium",
    LanguageName.MALAY: "medium",
    LanguageName.INDONESIAN: "medium",
    LanguageName.TAGALOG: "medium",
    LanguageName.SERBIAN: "medium",
    LanguageName.CROATIAN: "medium",
    LanguageName.BOSNIAN: "medium",
    LanguageName.BULGARIAN: "medium",
    LanguageName.SLOVENIAN: "medium",
    LanguageName.ALBANIAN: "medium",
    LanguageName.GEORGIAN: "medium",
    LanguageName.ARMENIAN: "medium",

    LanguageName.AZERBAIJANI: "rare",
    LanguageName.MONGOLIAN: "rare",
    LanguageName.LAO: "rare",
    LanguageName.KHMER: "rare",
    LanguageName.AMHARIC: "rare",
    LanguageName.TIGRINYA: "rare",
    LanguageName.SOMALI: "rare",
    LanguageName.ZULU: "rare",
    LanguageName.XHOSA: "rare",
    LanguageName.AFRIKAANS: "rare",
    LanguageName.SWAHILI: "rare",
    LanguageName.KINYARWANDA: "rare",
    LanguageName.KIRUNDI: "rare",
    LanguageName.WOLOF: "rare",
    LanguageName.HAUSA: "rare",
    LanguageName.YORUBA: "rare",
    LanguageName.IGBO: "rare",
    LanguageName.TWI: "rare",
    LanguageName.LUXEMBOURGISH: "rare",
    LanguageName.FAROESE: "rare",
    LanguageName.ICELANDIC: "rare",
    LanguageName.UZBEK: "rare",
    LanguageName.TAJIK: "rare",
    LanguageName.TURKMEN: "rare",
    LanguageName.KYRGYZ: "rare",
    LanguageName.KAZAKH: "rare",
    LanguageName.PASHTO: "rare",
    LanguageName.DARI: "rare",
    LanguageName.NEPALI: "rare",
    LanguageName.SINHALA: "rare",
    LanguageName.TAMIL: "rare",
    LanguageName.URDU: "rare",
    LanguageName.MACEDONIAN: "rare",
    LanguageName.BASQUE: "rare",
    LanguageName.CATALAN: "rare",
    LanguageName.GALICIAN: "rare",
    LanguageName.BELARUSIAN: "rare",
    LanguageName.TONGAN: "rare",
    LanguageName.SAMOAN: "rare",
    LanguageName.FIJIAN: "rare",
    LanguageName.BISLAMA: "rare",
    LanguageName.PALAUAN: "rare",
    LanguageName.MARSHALLESE: "rare",
    LanguageName.NAURUAN: "rare",
    LanguageName.NIUEAN: "rare",
    LanguageName.TOKELAUAN: "rare",
    LanguageName.GREENLANDIC: "rare",
    LanguageName.TAHITIAN: "rare",

    LanguageName.REUNION_FRENCH: "common",
    LanguageName.MAYOTTE_FRENCH: "common",
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

class InterpretationModel(BaseModel):
    src: LanguageName
    target: LanguageName
    type: Literal["Interpretation", "Consecutive Interpretation", "Simultaneous Interpretation"]
    uom: uom_time
    quantity: int


class TranslationRequest(BaseModel):
    jobs: list[TranslationModel | InterpretationModel]

class EstimateModel(BaseModel):
    total: float
    # Default to formula if we have historical data, else-wise use napkin math
    explaination: str

class TranslationResponse(BaseModel):
    estimates: list[EstimateModel]