import csv
from pathlib import Path
from typing import Dict, Any

from app.fetchers.translations._types import (
    NAPKIN_MATH_RATES,
    TranslationRequest, 
    TranslationResponse, 
    EstimateModel, 
    LANGUAGE_BANDS, 
    LanguageName,
    HistoricalData,
    parse_uom
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

def calculate_translation_cost(uom: str, quantity: int, src: LanguageName, target: LanguageName) -> tuple[float, str]:
    key = f"{src.value}_{target.value}_{uom}"
    
    if key in historical_rates and historical_rates[key]:
        rate = historical_rates[key]
        total = rate * quantity
        explanation = f"Historical data: avg rate ${rate:.3f} per {uom.lower()} × {quantity} = ${total:.2f}"
        return total, explanation
    
    target_band = LANGUAGE_BANDS[src] if LANGUAGE_BANDS[src] > LANGUAGE_BANDS[src] else LANGUAGE_BANDS[target]
    napkin_rate = NAPKIN_MATH_RATES[target_band]["translation"]
    total = napkin_rate * quantity
    explanation = f"Heuristic: ${napkin_rate} per word ({target_band} language) × {quantity} = ${total:.2f}"
    return total, explanation

def calculate_interpretation_cost(uom: str, quantity: int, src: LanguageName, target: LanguageName) -> tuple[float, str]:
    target_band = LANGUAGE_BANDS[src] if LANGUAGE_BANDS[src] > LANGUAGE_BANDS[src] else LANGUAGE_BANDS[target]
    napkin_rate = NAPKIN_MATH_RATES[target_band]["interpretation_hour"]
    
    if uom.lower() in ["day", "half day"]:
        hours = 8 if uom.lower() == "day" else 4
        total = napkin_rate * hours * quantity
        explanation = f"Heuristic: ${napkin_rate}/hour × {hours} hours × {quantity} {uom.lower()}(s) = ${total:.2f}"
    else:
        total = napkin_rate * quantity
        explanation = f"Heuristic: ${napkin_rate}/hour × {quantity} hours = ${total:.2f}"
    
    return total, explanation

def fetch_translations(req: TranslationRequest) -> TranslationResponse:
    estimates = []
    
    for job in req.jobs:
        if job.src == job.target:
            raise ValueError("Source and target languages cannot be the same.")

        if job.type == "Translation":
            total, explanation = calculate_translation_cost(job.uom, job.quantity, job.src, job.target)
            estimates.append(EstimateModel(total=total, explaination=explanation))

        elif job.type in ["Interpretation", "Consecutive Interpretation", "Simultaneous Interpretation"]:
            total, explanation = calculate_interpretation_cost(job.uom, job.quantity, job.src, job.target)
            estimates.append(EstimateModel(total=total, explaination=explanation))

    return TranslationResponse(estimates=estimates)
