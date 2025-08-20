from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from app.fetchers.per_diem.scrapers.exchange_rate import Currency

class Location(BaseModel):
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")

class CountryCode(str, Enum):
    AFGHANISTAN = "1149"
    ALBANIA = "1070"
    ALGERIA = "1150"
    ANDORRA = "1376"
    ANGOLA = "1176"
    ANGUILLA = "1463"
    ANTARCTICA = "1462"
    ANTIGUA_AND_BARBUDA = "1041"
    ARGENTINA = "1038"
    ARMENIA = "1071"
    ARUBA = "9988"
    ASCENSION_ISLAND = "1360"
    AUSTRALIA = "1118"
    AUSTRIA = "1072"
    AZERBAIJAN = "1073"
    BAHAMAS_THE = "1039"
    BAHRAIN = "1151"
    BANGLADESH = "1152"
    BARBADOS = "1045"
    BELARUS = "1357"
    BELGIUM = "1075"
    BELIZE = "1044"
    BENIN = "1186"
    BERMUDA = "1076"
    BHUTAN = "1379"
    BOLIVIA = "1040"
    BONAIRE_SINT_EUSTATIUS_SABA = "9989"
    BOSNIA_AND_HERZEGOVINA = "1361"
    BOTSWANA = "1178"
    BRAZIL = "1042"
    BRUNEI = "1119"
    BULGARIA = "1077"
    BURKINA_FASO = "1240"
    BURMA = "1120"
    BURUNDI = "1179"
    CABO_VERDE = "1181"
    CAMBODIA = "1122"
    CAMEROON = "1180"
    CANADA = "1079"
    CAYMAN_ISLANDS = "1464"
    CENTRAL_AFRICAN_REPUBLIC = "1182"
    CHAD = "1183"
    CHAGOS_ARCHIPELAGO = "1362"
    CHILE = "1046"
    CHINA = "1123"
    COCOS_KEELING_ISLANDS = "1382"
    COLOMBIA = "1047"
    COMOROS = "1184"
    COOK_ISLANDS = "1363"
    COSTA_RICA = "1048"
    COTE_DIVOIRE = "1194"
    CROATIA = "1358"
    CUBA = "1049"
    CURACAO = "9990"
    CYPRUS = "1081"
    CZECHIA = "1359"
    DPRK_NORTH_KOREA = "1429"
    DRC_CONGO = "1241"
    DENMARK = "1083"
    DJIBOUTI = "1175"
    DOMINICA = "1383"
    DOMINICAN_REPUBLIC = "1050"
    ECUADOR = "1051"
    EGYPT = "1154"
    EL_SALVADOR = "1052"
    EQUATORIAL_GUINEA = "1187"
    ERITREA = "1349"
    ESTONIA = "1084"
    ESWATINI = "1236"
    ETHIOPIA = "1188"
    FALKLAND_ISLANDS = "1385"
    FAROE_ISLANDS = "1386"
    FIJI = "1124"
    FINLAND = "1085"
    FRANCE = "1087"
    FRENCH_GUIANA = "1387"
    FRENCH_POLYNESIA = "1388"
    GABON = "1189"
    GAMBIA_THE = "1190"
    GEORGIA = "1088"
    GERMANY = "1089"
    GHANA = "1191"
    GIBRALTAR = "1390"
    GREECE = "1086"
    GREENLAND = "1364"
    GRENADA = "1055"
    GUADELOUPE = "1391"
    GUATEMALA = "1054"
    GUINEA = "1193"
    GUINEA_BISSAU = "1192"
    GUYANA = "1043"
    HAITI = "1056"
    HOLY_SEE = "1093"
    HONDURAS = "1057"
    HONG_KONG = "1126"
    HUNGARY = "1090"
    ICELAND = "1091"
    INDIA = "1155"
    INDONESIA = "1127"
    IRAN = "1392"
    IRAQ = "1157"
    IRELAND = "1247"
    ISRAEL = "1158"
    ITALY = "1092"
    JAMAICA = "1058"
    JAPAN = "1128"
    JORDAN = "1160"
    KAZAKHSTAN = "1094"
    KENYA = "1195"
    KIRIBATI = "1365"
    KOREA_SOUTH = "1129"
    KOSOVO = "1460"
    KUWAIT = "1161"
    KYRGYZSTAN = "1095"
    LAOS = "1130"
    LATVIA = "1096"
    LEBANON = "1162"
    LESOTHO = "1177"
    LIBERIA = "1196"
    LIBYA = "1398"
    LIECHTENSTEIN = "1400"
    LITHUANIA = "1097"
    LUXEMBOURG = "1098"
    MACAU = "1401"
    MADAGASCAR = "1197"
    MALAWI = "1199"
    MALAYSIA = "1131"
    MALDIVES = "1403"
    MALI = "1198"
    MALTA = "1099"
    MARSHALL_ISLANDS = "1146"
    MARTINIQUE = "1053"
    MAURITANIA = "1200"
    MAURITIUS = "1201"
    MAYOTTE = "1461"
    MEXICO = "1059"
    MICRONESIA = "1132"
    MOLDOVA = "1100"
    MONACO = "1404"
    MONGOLIA = "1133"
    MONTENEGRO = "1459"
    MONTSERRAT = "1467"
    MOROCCO = "1164"
    MOZAMBIQUE = "1227"
    NAMIBIA = "1232"
    NAURU = "1405"
    NEPAL = "1165"
    NETHERLANDS = "1101"
    NEW_CALEDONIA = "1406"
    NEW_ZEALAND = "1134"
    NICARAGUA = "1061"
    NIGER = "1228"
    NIGERIA = "1351"
    NIUE = "1407"
    NORTH_MACEDONIA = "1430"
    NORWAY = "1102"
    OMAN = "1167"
    OTHER_FOREIGN_LOCALITIES = "1375"
    PAKISTAN = "1166"
    PALAU = "1355"
    PANAMA = "1062"
    PAPUA_NEW_GUINEA = "1136"
    PARAGUAY = "1063"
    PERU = "1064"
    PHILIPPINES = "1139"
    POLAND = "1103"
    PORTUGAL = "1104"
    QATAR = "1168"
    REPUBLIC_OF_THE_CONGO = "1185"
    REUNION = "1428"
    ROMANIA = "1105"
    RUSSIA = "1106"
    RWANDA = "1229"
    SAINT_HELENA = "1366"
    SAINT_KITTS_AND_NEVIS = "1410"
    SAINT_VINCENT_AND_GRENADINES = "1413"
    SAMOA = "1140"
    SAN_MARINO = "1414"
    SAO_TOME_AND_PRINCIPE = "1353"
    SAUDI_ARABIA = "1169"
    SENEGAL = "1230"
    SERBIA = "1367"
    SEYCHELLES = "1242"
    SIERRA_LEONE = "1231"
    SINGAPORE = "1141"
    SINT_MAARTEN = "9987"
    SLOVAKIA = "1396"
    SLOVENIA = "1397"
    SOLOMON_ISLANDS = "1138"
    SOMALIA = "1249"
    SOUTH_AFRICA = "1233"
    SOUTH_SUDAN = "1345"
    SPAIN = "1107"
    SRI_LANKA = "1153"
    ST_LUCIA = "1411"
    SUDAN = "1235"
    SURINAME = "1065"
    SWEDEN = "1108"
    SWITZERLAND = "1109"
    SYRIA = "1170"
    TAIWAN = "1142"
    TAJIKISTAN = "1110"
    TANZANIA = "1237"
    THAILAND = "1143"
    TIMOR_LESTE = "1456"
    TOGO = "1238"
    TOKELAU = "1415"
    TONGA = "1137"
    TRINIDAD_AND_TOBAGO = "1066"
    TUNISIA = "1171"
    TURKEY = "1111"
    TURKMENISTAN = "1112"
    TURKS_AND_CAICOS_ISLANDS = "1418"
    TUVALU = "1356"
    UGANDA = "1239"
    UKRAINE = "1113"
    UNITED_ARAB_EMIRATES = "1172"
    UNITED_KINGDOM = "1114"
    UNITED_STATES = "-1"
    URUGUAY = "1067"
    UZBEKISTAN = "1115"
    VANUATU = "1421"
    VENEZUELA = "1069"
    VIETNAM = "1144"
    VIRGIN_ISLANDS_BRITISH = "1465"
    WALLIS_AND_FUTUNA = "1422"
    YEMEN = "1173"
    ZAMBIA = "1250"
    ZIMBABWE = "1234"

def make_country_name_enum():
    members = {name: name for name in CountryCode.__members__.keys()}
    return Enum("CountryName", members, type=str)

CountryName = make_country_name_enum()

def country_name_to_code_enum(country_name: CountryName) -> CountryCode:
    return CountryCode[country_name.value]

class USStateCode(str, Enum):
    AL = "AL"; AK = "AK"; AZ = "AZ"; AR = "AR"; CA = "CA"; CO = "CO"; CT = "CT"; DE = "DE"; FL = "FL"; GA = "GA"
    HI = "HI"; ID = "ID"; IL = "IL"; IN = "IN"; IA = "IA"; KS = "KS"; KY = "KY"; LA = "LA"; ME = "ME"; MD = "MD"
    MA = "MA"; MI = "MI"; MN = "MN"; MS = "MS"; MO = "MO"; MT = "MT"; NE = "NE"; NV = "NV"; NH = "NH"; NJ = "NJ"
    NM = "NM"; NY = "NY"; NC = "NC"; ND = "ND"; OH = "OH"; OK = "OK"; OR = "OR"; PA = "PA"; RI = "RI"; SC = "SC"
    SD = "SD"; TN = "TN"; TX = "TX"; UT = "UT"; VT = "VT"; VA = "VA"; WA = "WA"; WV = "WV"; WI = "WI"; WY = "WY"; DC = "DC"

COUNTRY_TO_CURRENCY: Dict[CountryCode, Currency] = {
    # A
    CountryCode.AFGHANISTAN: Currency.AFGHAN_AFGHANI,
    CountryCode.ALBANIA: Currency.ALBANIAN_LEK,
    CountryCode.ALGERIA: Currency.ALGERIAN_DINAR,
    CountryCode.ANDORRA: Currency.EURO,
    CountryCode.ANGOLA: Currency.ANGOLAN_KWANZA,
    CountryCode.ANGUILLA: Currency.EAST_CARIBBEAN_DOLLAR,
    CountryCode.ANTARCTICA: Currency.US_DOLLAR,
    CountryCode.ANTIGUA_AND_BARBUDA: Currency.EAST_CARIBBEAN_DOLLAR,
    CountryCode.ARGENTINA: Currency.ARGENTINE_PESO,
    CountryCode.ARMENIA: Currency.ARMENIAN_DRAM,
    CountryCode.ARUBA: Currency.ARUBAN_OR_DUTCH_GUILDER,
    CountryCode.ASCENSION_ISLAND: Currency.SAINT_HELENIAN_POUND,
    CountryCode.AUSTRALIA: Currency.AUSTRALIAN_DOLLAR,
    CountryCode.AUSTRIA: Currency.EURO,
    CountryCode.AZERBAIJAN: Currency.AZERBAIJAN_MANAT,

    # B
    CountryCode.BAHAMAS_THE: Currency.BAHAMIAN_DOLLAR,
    CountryCode.BAHRAIN: Currency.BAHRAINI_DINAR,
    CountryCode.BANGLADESH: Currency.BANGLADESHI_TAKA,
    CountryCode.BARBADOS: Currency.BARBADIAN_DOLLAR,
    CountryCode.BELARUS: Currency.BELARUSIAN_RUBLE_NEW,
    CountryCode.BELGIUM: Currency.EURO,
    CountryCode.BELIZE: Currency.BELIZEAN_DOLLAR,
    CountryCode.BENIN: Currency.CFA_FRANC,
    CountryCode.BERMUDA: Currency.BERMUDIAN_DOLLAR,
    CountryCode.BHUTAN: Currency.BHUTANESE_NGULTRUM,
    CountryCode.BOLIVIA: Currency.BOLIVIAN_BOLIVIANO,
    CountryCode.BONAIRE_SINT_EUSTATIUS_SABA: Currency.US_DOLLAR,
    CountryCode.BOSNIA_AND_HERZEGOVINA: Currency.BOSNIAN_CONVERTIBLE_MARK,
    CountryCode.BOTSWANA: Currency.BOTSWANA_PULA,
    CountryCode.BRAZIL: Currency.BRAZILIAN_REAL,
    CountryCode.BRUNEI: Currency.BRUNEIAN_DOLLAR,
    CountryCode.BULGARIA: Currency.BULGARIAN_LEV,
    CountryCode.BURKINA_FASO: Currency.CFA_FRANC,
    CountryCode.BURMA: Currency.BURMESE_KYAT,
    CountryCode.BURUNDI: Currency.BURUNDIAN_FRANC,

    # C
    CountryCode.CABO_VERDE: Currency.CAPE_VERDE_ESCUDO,
    CountryCode.CAMBODIA: Currency.CAMBODIAN_RIEL,
    CountryCode.CAMEROON: Currency.CENTRAL_AFRICAN_CFA,
    CountryCode.CANADA: Currency.CANADIAN_DOLLAR,
    CountryCode.CAYMAN_ISLANDS: Currency.CAYMAN_DOLLAR,
    CountryCode.CENTRAL_AFRICAN_REPUBLIC: Currency.CENTRAL_AFRICAN_CFA,
    CountryCode.CHAD: Currency.CENTRAL_AFRICAN_CFA,
    CountryCode.CHAGOS_ARCHIPELAGO: Currency.US_DOLLAR,
    CountryCode.CHILE: Currency.CHILEAN_PESO,
    CountryCode.CHINA: Currency.YUAN_RENMINBI,
    CountryCode.COCOS_KEELING_ISLANDS: Currency.AUSTRALIAN_DOLLAR,
    CountryCode.COLOMBIA: Currency.COLOMBIAN_PESO,
    CountryCode.COMOROS: Currency.COMORIAN_FRANC,
    CountryCode.COOK_ISLANDS: Currency.NEW_ZEALAND_DOLLAR,
    CountryCode.COSTA_RICA: Currency.COSTA_RICAN_COLON,
    CountryCode.COTE_DIVOIRE: Currency.CFA_FRANC,
    CountryCode.CROATIA: Currency.EURO,
    CountryCode.CUBA: Currency.CUBAN_PESO,
    CountryCode.CURACAO: Currency.DUTCH_GUILDER,
    CountryCode.CYPRUS: Currency.EURO,
    CountryCode.CZECHIA: Currency.CZECH_KORUNA,

    # D
    CountryCode.DPRK_NORTH_KOREA: Currency.NORTH_KOREAN_WON,
    CountryCode.DRC_CONGO: Currency.CONGOLESE_FRANC,
    CountryCode.DENMARK: Currency.DANISH_KRONE,
    CountryCode.DJIBOUTI: Currency.DJIBOUTIAN_FRANC,
    CountryCode.DOMINICA: Currency.EAST_CARIBBEAN_DOLLAR,
    CountryCode.DOMINICAN_REPUBLIC: Currency.DOMINICAN_PESO,

    # E
    CountryCode.ECUADOR: Currency.US_DOLLAR,
    CountryCode.EGYPT: Currency.EGYPTIAN_POUND,
    CountryCode.EL_SALVADOR: Currency.US_DOLLAR,
    CountryCode.EQUATORIAL_GUINEA: Currency.CENTRAL_AFRICAN_CFA,
    CountryCode.ERITREA: Currency.ERITREAN_NAKFA,
    CountryCode.ESTONIA: Currency.EURO,
    CountryCode.ESWATINI: Currency.SWAZI_LILANGENI,
    CountryCode.ETHIOPIA: Currency.ETHIOPIAN_BIRR,

    # F
    CountryCode.FALKLAND_ISLANDS: Currency.FALKLAND_ISLAND_POUND,
    CountryCode.FAROE_ISLANDS: Currency.DANISH_KRONE,
    CountryCode.FIJI: Currency.FIJIAN_DOLLAR,
    CountryCode.FINLAND: Currency.EURO,
    CountryCode.FRANCE: Currency.EURO,
    CountryCode.FRENCH_GUIANA: Currency.EURO,
    CountryCode.FRENCH_POLYNESIA: Currency.CFP_FRANC,

    # G
    CountryCode.GABON: Currency.CENTRAL_AFRICAN_CFA,
    CountryCode.GAMBIA_THE: Currency.GAMBIAN_DALASI,
    CountryCode.GEORGIA: Currency.GEORGIAN_LARI,
    CountryCode.GERMANY: Currency.EURO,
    CountryCode.GHANA: Currency.GHANAIAN_CEDI,
    CountryCode.GIBRALTAR: Currency.GIBRALTAR_POUND,
    CountryCode.GREECE: Currency.EURO,
    CountryCode.GREENLAND: Currency.DANISH_KRONE,
    CountryCode.GRENADA: Currency.EAST_CARIBBEAN_DOLLAR,
    CountryCode.GUADELOUPE: Currency.EURO,
    CountryCode.GUATEMALA: Currency.GUATEMALAN_QUETZAL,
    CountryCode.GUINEA: Currency.GUINEAN_FRANC,
    CountryCode.GUINEA_BISSAU: Currency.CFA_FRANC,
    CountryCode.GUYANA: Currency.GUYANESE_DOLLAR,

    # H
    CountryCode.HAITI: Currency.HAITIAN_GOURDE,
    CountryCode.HOLY_SEE: Currency.EURO,
    CountryCode.HONDURAS: Currency.HONDURAN_LEMPIRA,
    CountryCode.HONG_KONG: Currency.HONG_KONG_DOLLAR,
    CountryCode.HUNGARY: Currency.HUNGARIAN_FORINT,

    # I
    CountryCode.ICELAND: Currency.ICELANDIC_KRONA,
    CountryCode.INDIA: Currency.INDIAN_RUPEE,
    CountryCode.INDONESIA: Currency.INDONESIAN_RUPIAH,
    CountryCode.IRAN: Currency.IRANIAN_RIAL,
    CountryCode.IRAQ: Currency.IRAQI_DINAR,
    CountryCode.IRELAND: Currency.EURO,
    CountryCode.ISRAEL: Currency.ISRAELI_SHEKEL,
    CountryCode.ITALY: Currency.EURO,

    # J
    CountryCode.JAMAICA: Currency.JAMAICAN_DOLLAR,
    CountryCode.JAPAN: Currency.JAPANESE_YEN,
    CountryCode.JORDAN: Currency.JORDANIAN_DINAR,

    # K
    CountryCode.KAZAKHSTAN: Currency.KAZAKH_TENGE,
    CountryCode.KENYA: Currency.KENYAN_SHILLING,
    CountryCode.KIRIBATI: Currency.AUSTRALIAN_DOLLAR,
    CountryCode.KOREA_SOUTH: Currency.SOUTH_KOREAN_WON,
    CountryCode.KOSOVO: Currency.EURO,
    CountryCode.KUWAIT: Currency.KUWAITI_DINAR,
    CountryCode.KYRGYZSTAN: Currency.KYRGYZSTANI_SOM,

    # L
    CountryCode.LAOS: Currency.LAO_KIP,
    CountryCode.LATVIA: Currency.EURO,
    CountryCode.LEBANON: Currency.LEBANESE_POUND,
    CountryCode.LESOTHO: Currency.BASOTHO_LOTI,
    CountryCode.LIBERIA: Currency.LIBERIAN_DOLLAR,
    CountryCode.LIBYA: Currency.LIBYAN_DINAR,
    CountryCode.LIECHTENSTEIN: Currency.SWISS_FRANC,
    CountryCode.LITHUANIA: Currency.EURO,
    CountryCode.LUXEMBOURG: Currency.EURO,

    # M
    CountryCode.MACAU: Currency.MACAU_PATACA,
    CountryCode.MADAGASCAR: Currency.MALAGASY_ARIARY,
    CountryCode.MALAWI: Currency.MALAWIAN_KWACHA,
    CountryCode.MALAYSIA: Currency.MALAYSIAN_RINGGIT,
    CountryCode.MALDIVES: Currency.MALDIVIAN_RUFIYAA,
    CountryCode.MALI: Currency.CFA_FRANC,
    CountryCode.MALTA: Currency.EURO,
    CountryCode.MARSHALL_ISLANDS: Currency.US_DOLLAR,
    CountryCode.MARTINIQUE: Currency.EURO,
    CountryCode.MAURITANIA: Currency.MAURITANIAN_OUGUIYA,
    CountryCode.MAURITIUS: Currency.MAURITIAN_RUPEE,
    CountryCode.MAYOTTE: Currency.EURO,
    CountryCode.MEXICO: Currency.MEXICAN_PESO,
    CountryCode.MICRONESIA: Currency.US_DOLLAR,
    CountryCode.MOLDOVA: Currency.MOLDOVAN_LEU,
    CountryCode.MONACO: Currency.EURO,
    CountryCode.MONGOLIA: Currency.MONGOLIAN_TUGRIK,
    CountryCode.MONTENEGRO: Currency.EURO,
    CountryCode.MONTSERRAT: Currency.EAST_CARIBBEAN_DOLLAR,
    CountryCode.MOROCCO: Currency.MOROCCAN_DIRHAM,
    CountryCode.MOZAMBIQUE: Currency.MOZAMBICAN_METICAL,

    # N
    CountryCode.NAMIBIA: Currency.NAMIBIAN_DOLLAR,
    CountryCode.NAURU: Currency.AUSTRALIAN_DOLLAR,
    CountryCode.NEPAL: Currency.NEPALESE_RUPEE,
    CountryCode.NETHERLANDS: Currency.EURO,
    CountryCode.NEW_CALEDONIA: Currency.CFP_FRANC,
    CountryCode.NEW_ZEALAND: Currency.NEW_ZEALAND_DOLLAR,
    CountryCode.NICARAGUA: Currency.NICARAGUAN_CORDOBA,
    CountryCode.NIGER: Currency.CFA_FRANC,
    CountryCode.NIGERIA: Currency.NIGERIAN_NAIRA,
    CountryCode.NIUE: Currency.NEW_ZEALAND_DOLLAR,
    CountryCode.NORTH_MACEDONIA: Currency.MACEDONIAN_DENAR,
    CountryCode.NORWAY: Currency.NORWEGIAN_KRONE,

    # O
    CountryCode.OMAN: Currency.OMANI_RIAL,
    CountryCode.OTHER_FOREIGN_LOCALITIES: Currency.US_DOLLAR,  # sensible default

    # P
    CountryCode.PAKISTAN: Currency.PAKISTANI_RUPEE,
    CountryCode.PALAU: Currency.US_DOLLAR,
    CountryCode.PANAMA: Currency.PANAMANIAN_BALBOA,            # PAB (USD also used)
    CountryCode.PAPUA_NEW_GUINEA: Currency.PAPUA_KINA,
    CountryCode.PARAGUAY: Currency.PARAGUAYAN_GUARANI,
    CountryCode.PERU: Currency.PERUVIAN_SOL,
    CountryCode.PHILIPPINES: Currency.PHILIPPINE_PESO,
    CountryCode.POLAND: Currency.POLISH_ZLOTY,
    CountryCode.PORTUGAL: Currency.EURO,
    CountryCode.QATAR: Currency.QATARI_RIYAL,

    # R
    CountryCode.REPUBLIC_OF_THE_CONGO: Currency.CENTRAL_AFRICAN_CFA,  # Congo (Brazzaville)
    CountryCode.REUNION: Currency.EURO,
    CountryCode.ROMANIA: Currency.ROMANIAN_LEU,
    CountryCode.RUSSIA: Currency.RUSSIAN_RUBLE,
    CountryCode.RWANDA: Currency.RWANDAN_FRANC,

    # S
    CountryCode.SAINT_HELENA: Currency.SAINT_HELENIAN_POUND,
    CountryCode.SAINT_KITTS_AND_NEVIS: Currency.EAST_CARIBBEAN_DOLLAR,
    CountryCode.SAINT_VINCENT_AND_GRENADINES: Currency.EAST_CARIBBEAN_DOLLAR,
    CountryCode.SAMOA: Currency.SAMOAN_TALA,
    CountryCode.SAN_MARINO: Currency.EURO,
    CountryCode.SAO_TOME_AND_PRINCIPE: Currency.SAO_TOME_DOBRA,
    CountryCode.SAUDI_ARABIA: Currency.SAUDI_RIYAL,
    CountryCode.SENEGAL: Currency.CFA_FRANC,
    CountryCode.SERBIA: Currency.SERBIAN_DINAR,
    CountryCode.SEYCHELLES: Currency.SEYCHELLOIS_RUPEE,
    CountryCode.SIERRA_LEONE: Currency.SIERRA_LEONEAN_LEONE,
    CountryCode.SINGAPORE: Currency.SINGAPORE_DOLLAR,
    CountryCode.SINT_MAARTEN: Currency.DUTCH_GUILDER,          # ANG
    CountryCode.SLOVAKIA: Currency.EURO,                       # (replaced SKK)
    CountryCode.SLOVENIA: Currency.EURO,
    CountryCode.SOLOMON_ISLANDS: Currency.SOLOMON_DOLLAR,
    CountryCode.SOMALIA: Currency.SOMALI_SHILLING,
    CountryCode.SOUTH_AFRICA: Currency.SOUTH_AFRICAN_RAND,
    CountryCode.SOUTH_SUDAN: Currency.SUDANESE_POUND,          # SSP not in enum; closest available
    CountryCode.SPAIN: Currency.EURO,
    CountryCode.SRI_LANKA: Currency.SRI_LANKAN_RUPEE,
    CountryCode.ST_LUCIA: Currency.EAST_CARIBBEAN_DOLLAR,
    CountryCode.SUDAN: Currency.SUDANESE_POUND,
    CountryCode.SURINAME: Currency.SURINAMESE_DOLLAR,
    CountryCode.SWEDEN: Currency.SWEDISH_KRONA,
    CountryCode.SWITZERLAND: Currency.SWISS_FRANC,
    CountryCode.SYRIA: Currency.SYRIAN_POUND,

    # T
    CountryCode.TAIWAN: Currency.TAIWAN_DOLLAR,
    CountryCode.TAJIKISTAN: Currency.TAJIK_SOMONI,
    CountryCode.TANZANIA: Currency.TANZANIAN_SHILLING,
    CountryCode.THAILAND: Currency.THAI_BAHT,
    CountryCode.TIMOR_LESTE: Currency.US_DOLLAR,
    CountryCode.TOGO: Currency.CFA_FRANC,
    CountryCode.TOKELAU: Currency.NEW_ZEALAND_DOLLAR,
    CountryCode.TONGA: Currency.TONGAN_PAANGA,
    CountryCode.TRINIDAD_AND_TOBAGO: Currency.TRINIDADIAN_DOLLAR,
    CountryCode.TUNISIA: Currency.TUNISIAN_DINAR,
    CountryCode.TURKEY: Currency.TURKISH_LIRA,
    CountryCode.TURKMENISTAN: Currency.TURKMEN_MANAT,
    CountryCode.TURKS_AND_CAICOS_ISLANDS: Currency.US_DOLLAR,
    CountryCode.TUVALU: Currency.TUVALUAN_DOLLAR,              # often AUD in practice; enum has TVD

    # U
    CountryCode.UGANDA: Currency.UGANDAN_SHILLING,
    CountryCode.UKRAINE: Currency.UKRAINIAN_HRYVNIA,
    CountryCode.UNITED_ARAB_EMIRATES: Currency.EMIRATI_DIRHAM,
    CountryCode.UNITED_KINGDOM: Currency.BRITISH_POUND,
    CountryCode.UNITED_STATES: Currency.US_DOLLAR,
    CountryCode.URUGUAY: Currency.URUGUAYAN_PESO,
    CountryCode.UZBEKISTAN: Currency.UZBEK_SOM,

    # V
    CountryCode.VANUATU: Currency.VANUATU_VATU,
    CountryCode.VENEZUELA: Currency.VENEZUELAN_BOLIVAR,
    CountryCode.VIETNAM: Currency.VIETNAMESE_DONG,
    CountryCode.VIRGIN_ISLANDS_BRITISH: Currency.US_DOLLAR,
    CountryCode.WALLIS_AND_FUTUNA: Currency.CFP_FRANC,

    # Y, Z
    CountryCode.YEMEN: Currency.YEMENI_RIAL,
    CountryCode.ZAMBIA: Currency.ZAMBIAN_KWACHA,
    CountryCode.ZIMBABWE: Currency.ZIMBABWEAN_DOLLAR,
}