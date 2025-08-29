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
        "Estimate ground transportation costs accurately for each request.\n"
        "Consider location-based pricing adjustments for remote locations.\n"
        "Round all USD amounts to whole dollars."
    )

    lines.append("\nRequests:\n")

    for i, p in enumerate(req.ground_transport_data, start=1):
        lines.extend([
            f"Request {i}",
            f"Country {p.country}",
            f"Vehicle type {p.vehicle_type}",
            f"Airport arrival {p.airport_arrival}",
            f"Airport departure {p.airport_departure}",
            f"Outside city limits rate {p.outside_city_limits_rate}",
            f"rate_type {p.rate_type}"
        ])
        lines.append("")
    
    lines.append("For each request, return JSON that matches the expected schema, followed by a brief explanation.")

    return "\n".join(lines)

def get_ground_transport_estimate(req: GroundTransportRequest):
    system_prompt = (
        "You are a careful ground transportation cost estimator."
        "Follow your instructions closely and use up-to-date information."
        "Return your response as JSON containing the following fields:"
        "cost(int) - The total estimated cost of the service"
        "explanation(str) - A brief explanation of the cost estimation."
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