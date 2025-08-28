from app.fetchers.openai import client
from typing import List
from pydantic import BaseModel

from app.fetchers._types import LLMResponseModel

class EquipmentModel(BaseModel):
    location: str
    duration_days: int
    
    # Individual quantity fields for each equipment type
    laptop: int = 0
    portable_printer: int = 0
    large_printer: int = 0
    projector: int = 0
    equipment_other: int = 0
    cell_phone: int = 0
    cell_phone_minutes: int = 0  # in minutes
    hot_spot: int = 0
    satellite_phone: int = 0
    locator_beacon: int = 0
    setup_and_cleanup: bool = False
    onsite_support_equipment: bool = False
    
    equipment_other_description: str = ""

class EquipmentRequest(BaseModel):
    equipment_data: List[EquipmentModel]

def build_prompt(req: EquipmentRequest) -> str:
    lines: List[str] = []

    lines.append(
        "Estimate equipment rental and support costs accurately for each request.\n"
        "Use daily rental rates for equipment, setup fees for initial setup, and hourly rates for onsite support.\n"
        "Consider location-based pricing adjustments for remote or international locations.\n"
        "If an item quantity is 0 or service isn't requested, price it at $0.\n"
        "Round all USD amounts to whole dollars."
    )

    lines.append("\nRequests:\n")
    for i, e in enumerate(req.equipment_data, start=1):
        lines.extend([
            f"Request {i}:",
            f"- Location: {e.location}",
            f"- Duration: {e.duration_days} days",
        ])
        
        # Only include equipment types with non-zero quantities
        equipment_items = [
            ("Laptops", e.laptop),
            ("Portable Printers", e.portable_printer),
            ("Large Printers", e.large_printer),
            ("Projectors", e.projector),
            ("Equipment - Other", e.equipment_other),
            ("Cell Phones", e.cell_phone),
            ("Cell Phone Minutes", e.cell_phone_minutes),
            ("Hot Spots", e.hot_spot),
            ("Satellite Phones", e.satellite_phone),
            ("Locator Beacons", e.locator_beacon),
        ]
        
        for item_name, quantity in equipment_items:
            if quantity > 0:
                if item_name == "Cell Phone Minutes":
                    lines.append(f"- {item_name}: {quantity} minutes")
                else:
                    lines.append(f"- {item_name}: {quantity}")
        
        lines.append(f"- Setup and Cleanup: {'yes' if e.setup_and_cleanup else 'no'}")
        lines.append(f"- Onsite Support - Equipment: {'yes' if e.onsite_support_equipment else 'no'}")
        
        if e.equipment_other > 0 and e.equipment_other_description:
            lines.append(f"- Other equipment description: {e.equipment_other_description}")
        lines.append("")

    lines.append(
        "For each request, return JSON that matches the expected schema, followed by a brief explanation. "
        "Show simple math for each line (rate × quantity × duration). Ensure the total equals the sum of "
        "equipment rental, setup fees, and support costs."
    )

    return "\n".join(lines)


class EquipmentResponseModel(BaseModel):
    res: list[LLMResponseModel]

def get_equipment_estimate(req: EquipmentRequest) -> List[LLMResponseModel]:
    system_msg = (
        "You are a careful equipment rental cost estimator. "
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
        text_format=EquipmentResponseModel,
        temperature=0.2,
        top_p=1,
        max_output_tokens=900,
    )

    parsed = response.output_parsed
    out = ([LLMResponseModel(cost=0, explanation="Unable to parse response")]
           if not parsed else parsed.res)

    return _sanity_check(out)

def _sanity_check(items: List[LLMResponseModel]) -> List[LLMResponseModel]:
    checked: List[LLMResponseModel] = []
    for it in items:
        if it.cost is None or it.cost < 0:
            it.cost = 0
            it.explanation = (it.explanation or "") + "\n[Note] Adjusted invalid negative/None cost to $0."
        checked.append(it)
    return checked