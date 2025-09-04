import csv
from pathlib import Path
import statistics
from typing import Dict, Any, Literal

from app.fetchers.translations._types import (
    BASE_RATES,
    COUNTRY_MULTIPLIERS,
    TranslationRequest, 
    TranslationResponse, 
    EstimateModel, 
    LANGUAGE_BANDS, 
    LanguageName,
    HistoricalData,
    parse_uom,
    BandLiteral,
    uom_words,
    uom_time,
    translation_type
)

CSV_FILE_PATH = Path(__file__).parent / "VendorRates.csv"

historical_rates = {}

def load_historical_data() -> Dict[str, Any]:
    print("Loading historical data from CSV...")

    if not CSV_FILE_PATH.exists():
        print(f"CSV file not found at {CSV_FILE_PATH}. Using heuristics...")
        return {}
    
    try:
        skips = 0

        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    validated_data = HistoricalData.model_validate(row)

                    cleaned_uom = parse_uom(
                        validated_data.uom
                    )

                    if cleaned_uom is None:
                        raise ValueError(f"Invalid UoM: {validated_data.uom}")

                    key = f"{validated_data.src.value}_{validated_data.target.value}_{cleaned_uom}"
                    if key not in historical_rates:
                        historical_rates[key] = []
                    historical_rates[key].append(validated_data.vendor_rate)

                    # This implies rates are bi-directional
                    if row.get("Translation Direction") == "To / From":
                        key = f"{validated_data.target.value}_{validated_data.src.value}_{cleaned_uom}"
                        if key not in historical_rates:
                            historical_rates[key] = []
                        historical_rates[key].append(validated_data.vendor_rate)

                except Exception as e:
                    skips += 1
                    # print(e)
                    continue

            for key, values in historical_rates.items():
                historical_rates[key] = round(sum(values) / len(values), 2)

            print(f"Loaded historical rates for {len(historical_rates)} language pairs.")
            print(f"Skipped {skips} rows due to errors.")

    except Exception as e:
        print(f"Error loading historical data: {e}")
        return {}
    
    return historical_rates

load_historical_data()

def get_country_multiplier(country: str) -> float:
    """Get country-based rate multiplier"""
    return COUNTRY_MULTIPLIERS.get(country.upper(), COUNTRY_MULTIPLIERS["DEFAULT"])

def get_language_tier(src: LanguageName, target: LanguageName) -> BandLiteral:
    """Get the highest tier between source and target languages"""
    src_tier = LANGUAGE_BANDS[src]
    target_tier = LANGUAGE_BANDS[target]
    
    # Return the higher tier (tier4 > tier3 > tier2 > tier1)
    tier_order = {"tier1": 1, "tier2": 2, "tier3": 3, "tier4": 4}
    if tier_order[src_tier] > tier_order[target_tier]:
        return src_tier
    return target_tier

def calculate_translation_cost(
    uom: uom_words, 
    quantity: int, 
    src: LanguageName, 
    target: LanguageName,
    country: str = "US",
    provider_type: Literal["freelancer", "agency"] = "freelancer",
    urgency: Literal["standard", "rush"] = "standard",
    volume_discount: bool = False
) -> tuple[float, str]:
    key = f"{src.value}_{target.value}_{uom}"
    
    # Try historical data first
    if key in historical_rates and historical_rates[key]:
        base_rate = historical_rates[key]
        explanation_parts = [f"Historical data: ${base_rate:.3f} per {uom.lower()}"]
    else:
        # Use industry-aligned rates
        tier = get_language_tier(src, target)
        rate_range = BASE_RATES[tier]["translation"]
        base_rate = statistics.mean([rate_range["min"], rate_range["max"]])
        explanation_parts = [f"Industry rate: ${base_rate:.3f} per word ({tier} language)"]
    
    # Apply country multiplier
    country_mult = get_country_multiplier(country)
    rate_after_country = base_rate * country_mult
    if country_mult != 1.0:
        explanation_parts.append(f"Country adjustment ({country}): ×{country_mult:.2f}")
    
    # Apply provider markup
    if provider_type == "agency":
        agency_markup = 1.35  # 35% average markup
        rate_after_provider = rate_after_country * agency_markup
        explanation_parts.append(f"Agency markup: ×{agency_markup:.2f}")
    else:
        rate_after_provider = rate_after_country
    
    # Apply urgency premium
    if urgency == "rush":
        rush_premium = 1.35  # 35% average rush premium
        rate_after_urgency = rate_after_provider * rush_premium
        explanation_parts.append(f"Rush premium: ×{rush_premium:.2f}")
    else:
        rate_after_urgency = rate_after_provider
    
    # Calculate subtotal
    subtotal = rate_after_urgency * quantity
    
    # Apply volume discount
    if volume_discount and quantity >= 5000:
        discount = 0.15  # 15% volume discount
        total = subtotal * (1 - discount)
        explanation_parts.append(f"Volume discount (-{discount*100:.0f}%): ${subtotal:.2f} → ${total:.2f}")
    else:
        total = subtotal
    
    explanation = " | ".join(explanation_parts) + f" × {quantity} = ${total:.2f}"
    return total, explanation

def calculate_interpretation_cost(
    service_type: translation_type,
    uom: uom_time, 
    quantity: int, 
    src: LanguageName, 
    target: LanguageName,
    country: str = "US",
    provider_type: Literal["freelancer", "agency"] = "freelancer",
    urgency: Literal["standard", "rush"] = "standard"
) -> tuple[float, str]:
    tier = get_language_tier(src, target)
    
    # Determine service type for rate lookup
    if service_type == "Simultaneous Interpretation":
        service_key = "simultaneous_interpretation"
    else:
        service_key = "consecutive_interpretation"
    
    rate_range = BASE_RATES[tier][service_key]
    base_hourly_rate = statistics.mean([rate_range["min"], rate_range["max"]])
    
    explanation_parts = [f"Industry rate: ${base_hourly_rate:.0f}/hour ({tier} {service_key.replace('_', ' ')})"]
    
    # Apply country multiplier
    country_mult = get_country_multiplier(country)
    rate_after_country = base_hourly_rate * country_mult
    if country_mult != 1.0:
        explanation_parts.append(f"Country adjustment ({country}): ×{country_mult:.2f}")
    
    # Apply provider markup
    if provider_type == "agency":
        agency_markup = 1.35
        rate_after_provider = rate_after_country * agency_markup
        explanation_parts.append(f"Agency markup: ×{agency_markup:.2f}")
    else:
        rate_after_provider = rate_after_country
    
    # Apply urgency premium
    if urgency == "rush":
        rush_premium = 1.35
        rate_after_urgency = rate_after_provider * rush_premium
        explanation_parts.append(f"Rush premium: ×{rush_premium:.2f}")
    else:
        rate_after_urgency = rate_after_provider
    
    # Calculate total based on UOM
    if uom.lower() in ["day", "half day"]:
        hours = 8 if uom.lower() == "day" else 4
        total = rate_after_urgency * hours * quantity
        explanation_parts.append(f"× {hours} hours × {quantity} {uom.lower()}(s) = ${total:.2f}")
    else:
        total = rate_after_urgency * quantity
        explanation_parts.append(f"× {quantity} hours = ${total:.2f}")
    
    explanation = " | ".join(explanation_parts)
    return total, explanation

def fetch_translations(req: TranslationRequest) -> TranslationResponse:
    estimates = []
    
    for job in req.jobs:
        if job.src == job.target:
            raise ValueError("Source and target languages cannot be the same.")

        if job.type == "Translation":
            total, explanation = calculate_translation_cost(
                job.uom, job.quantity, job.src, job.target,
                job.country or "US", job.provider_type, job.urgency, job.volume_discount
            )
            estimates.append(EstimateModel(total=total, explaination=explanation))

        elif job.type in ["Interpretation", "Consecutive Interpretation", "Simultaneous Interpretation"]:
            total, explanation = calculate_interpretation_cost(
                job.type, job.uom, job.quantity, job.src, job.target,
                job.country or "US", job.provider_type, job.urgency
            )
            estimates.append(EstimateModel(total=total, explaination=explanation))

    return TranslationResponse(estimates=estimates)
