from app.fetchers.openai import client
from pydantic import BaseModel
from typing import List
from app.fetchers._types import  LLMResponseModel

 
class VisaModel(BaseModel):
    service_type: str
    from_date: str
    to_date: str
    from_country: str
    to_country: str

class VisaRequest(BaseModel):
    visa_data: List[VisaModel]

class VisaResponseModel(BaseModel):
    res: List[LLMResponseModel]


def build_prompt(req: VisaRequest):
    lines: List[str] = []

    lines.append(
        "Estimate visa costs accurately using official government fees and processing charges.\n"
        "Use current State Department and embassy fee schedules as baseline.\n"
        "Add realistic processing service fees for expedited handling.\n"
        "Consider location-based pricing adjustments for remote locations.\n"
        "Round all USD amounts to whole dollars.\n"
        "Visas are always considered business visas.\n"
        "\n"
        "IMPORTANT: Base estimates on official fees, not inflated service charges.\n"
        "Reference baseline costs:\n"
        "- US B1/B2 visa: $185 (government fee) + $50-150 (processing fee)\n"
        "- Schengen visa: €80 ($85-90) + $50-100 (processing fee)\n"
        "- UK business visa: £100 ($125) + $75-150 (processing fee)\n"
        "- Other countries: Research current official rates\n"
        "- Emergency/rush processing: Add 50-100% premium"
    )

    lines.append("\nRequests:\n")

    for i, p in enumerate(req.visa_data, start=1):
        lines.extend([
            f"Request {i}:",
            f"Service: {p.service_type}",
            f"From date: {p.from_date}",
            f"To date: {p.to_date}",
            f"From country: {p.from_country}",
            f"To country: {p.to_country}"
        ])
        
        lines.append("")
    
    lines.append("For each request, return JSON that matches the expected schema, followed by a brief explanation showing official fee + processing breakdown.")

    return "\n".join(lines)


def get_visa_estimate(req: VisaRequest):
    system_prompt = (
        "You are a careful visa services estimator with access to current official government fee schedules. "
        "Always base estimates on official embassy/consulate fees plus reasonable processing charges. "
        "Follow your instructions closely and use up-to-date official information. "
        "Return your response as JSON containing the following fields: "
        "cost(int) - The total estimated cost of the service "
        "explanation(str) - A brief explanation showing official fee + processing breakdown."
    )
    user_prompt = build_prompt(req)

    response = client.responses.parse(
        model="gpt-4.1-2025-04-14",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text_format=VisaResponseModel,
        temperature=0.2,
        top_p=1,
        max_output_tokens=900,
    )

    parsed = response.output_parsed
    out = ([LLMResponseModel(cost=0, explanation="Unable to parse response")]
           if not parsed else parsed.res)

    return out


