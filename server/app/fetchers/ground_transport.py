from app.fetchers.openai import client
from pydantic import BaseModel
from typing import List
from app.fetchers._types import LLMResponseModel

# Fill in your fields for GroundTransportModel
class GroundTransportModel(BaseModel):
    country: str
    vehicle_type: str
    airport_arrival: bool
    airport_departure: bool
    outside_city_limits_rate: bool
    rate_type: str

class GroundTransportRequest(BaseModel):
    ground_transport_data: List[GroundTransportModel]

class GroundTransportResponseModel(BaseModel):
    res: List[LLMResponseModel]

def build_prompt(req: GroundTransportRequest):
    lines: List[str] = []

    lines.append(
        "Estimate ground transportation costs accurately for each request using current market rates.\n"
        "IMPORTANT: Use realistic commercial rates, not economy/budget pricing.\n"
        "Consider location-based pricing adjustments for remote locations.\n"
        "Apply premium city multipliers: NYC/SF/DC (+50%), international cities (+30%).\n"
        "Airport transfers include mandatory surcharges and tolls.\n"
        "Hourly rates should reflect professional chauffeur services, not rideshare.\n"
        "Round all USD amounts to whole dollars.\n"
        "\n"
        "Reference rates by vehicle type:\n"
        "- Sedan/Car: $80-120/hour in major cities, $60-90 elsewhere\n"
        "- SUV/Large Vehicle: $100-150/hour in major cities, $80-120 elsewhere\n"
        "- Van/Bus: $120-200/hour depending on capacity\n"
        "- Airport transfers: Add $20-50 surcharge for tolls/fees\n"
        "- Outside city limits: Add 25-50% surcharge for distance"
    )

    lines.append("\nRequests:\n")

    for i, p in enumerate(req.ground_transport_data, start=1):
        lines.extend([
            f"Request {i}:",
            f"Country: {p.country}",
            f"Vehicle type: {p.vehicle_type}",
            f"Airport arrival: {p.airport_arrival}",
            f"Airport departure: {p.airport_departure}",
            f"Outside city limits rate: {p.outside_city_limits_rate}",
            f"Rate type: {p.rate_type}"
        ])
        lines.append("")
    
    lines.append("For each request, return JSON that matches the expected schema, followed by a brief explanation showing your rate calculation.")

    return "\n".join(lines)

def get_ground_transport_estimate(req: GroundTransportRequest):
    system_prompt = (
        "You are a careful ground transportation cost estimator specializing in commercial/professional transport services. "
        "Use current market rates for professional chauffeur and corporate transportation services. "
        "NEVER use economy/budget pricing - always use commercial service rates. "
        "Follow your instructions closely and use up-to-date information. "
        "Return your response as JSON containing the following fields: "
        "cost(int) - The total estimated cost of the service "
        "explanation(str) - A brief explanation of the cost estimation including rate calculation."
    )
    user_prompt = build_prompt(req)

    response = client.responses.parse(
        model="gpt-4.1-2025-04-14",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text_format=GroundTransportResponseModel,
        temperature=0.2,
        top_p=1,
        max_output_tokens=900,
    )

    parsed = response.output_parsed
    out = ([LLMResponseModel(cost=0, explanation="Unable to parse response")]
           if not parsed else parsed.res)

    return out