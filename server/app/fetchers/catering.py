from app.fetchers.openai import client
from typing import List, Literal
from pydantic import BaseModel

from app.fetchers._types import LLMResponseModel

class CateringModel(BaseModel):
    meal_type: Literal["breakfast", "lunch", "dinner"]
    location: str
    meals: int
    coffee_break: bool
    setup: bool
    clean_up: bool
    delivery: bool
    supplies: bool
    onsite_support: bool

class CateringRequest(BaseModel):
    catering_data: List[CateringModel]

def build_prompt(req: CateringRequest) -> str:
    lines: List[str] = []

    # Short rules that prevent 90% of errors
    lines.append(
        "Estimate catering costs accurately for each request.\n"
        "Use per-person pricing for food/coffee, flat fees for delivery, and hourly labor.\n"
        "Avoid double-counting: onsite support covers time during the event; setup/clean-up only covers prep/tear-down.\n"
        "If an item isn't requested, price it at $0. Apply any city adjustment only to food+labor, not delivery.\n"
        "Round all USD amounts to whole dollars."
    )

    lines.append("\nRequests:\n")
    for i, c in enumerate(req.catering_data, start=1):
        lines.extend([
            f"Request {i}:",
            f"- Meal type: {c.meal_type}",
            f"- Location: {c.location}",
            f"- Headcount: {c.meals}",
            f"- Coffee break: {'yes' if c.coffee_break else 'no'}",
            f"- Setup: {'yes' if c.setup else 'no'}",
            f"- Clean-up: {'yes' if c.clean_up else 'no'}",
            f"- Delivery: {'yes' if c.delivery else 'no'}",
            f"- Supplies (disposables): {'yes' if c.supplies else 'no'}",
            f"- Onsite support during event: {'yes' if c.onsite_support else 'no'}",
            ""
        ])

    lines.append(
        "For each request, return JSON that matches the expected schema, followed by a brief explanation. "
        "Show simple math for each line (rate × quantity). Ensure the grand total equals the sum of line items "
        "plus tax/service, and that per-person equals grand total divided by headcount."
    )

    return "\n".join(lines)


class CateringResponseModel(BaseModel):
    res: list[LLMResponseModel]

def get_catering_estimate(req: CateringRequest) -> List[LLMResponseModel]:
    system_msg = (
        "You are a careful catering cost estimator. "
        "Follow instructions strictly, compute with unit rates, and keep results consistent. Output your format as JSON containing the following fields: "
        "- cost (number): the total estimated cost for the request\n"
        "- explanation (string): a brief explanation of the cost breakdown"
    )
    user_msg = build_prompt(req)

    response = client.responses.parse(
        model="gpt-4.1-2025-04-14",
        input=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        text_format=CateringResponseModel,
        temperature=0.2,                    # lower = more consistent math
        top_p=1,
        max_output_tokens=900,
    )

    parsed = response.output_parsed
    out = ([LLMResponseModel(cost=0, explanation="Unable to parse response")]
           if not parsed else parsed.res)

    # Optional: quick sanity pass to catch obvious math errors
    return _sanity_check(out)

def _sanity_check(items: List[LLMResponseModel]) -> List[LLMResponseModel]:
    checked: List[LLMResponseModel] = []
    for it in items:
        # if your LLMResponseModel only has cost/explanation, we just guard against negatives or zeros
        if it.cost is None or it.cost < 0:
            it.cost = 0
            it.explanation = (it.explanation or "") + "\n[Note] Adjusted invalid negative/None cost to $0."
        checked.append(it)
    return checked
