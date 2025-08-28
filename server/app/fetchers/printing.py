from app.fetchers.openai import client
from typing import List
from pydantic import BaseModel

from app.fetchers._types import LLMResponseModel

class PrintingModel(BaseModel):
    location: str
    
    # Printing quantities
    bw_single_sided: int = 0  # pages
    bw_double_sided: int = 0  # pages
    color_single_sided: int = 0  # pages
    color_double_sided: int = 0  # pages
    
    # Production quantities
    certificate_card_stock: int = 0
    simple_frame: int = 0
    name_tag_cardstock_with_lanyard: int = 0
    table_tent_cardstock: int = 0
    
    # Materials - Other quantities
    binding_spiral_bound_with_dividers: int = 0
    binding_3ring_binder_with_dividers: int = 0
    
    # Services
    delivery: bool = False

class PrintingRequest(BaseModel):
    printing_data: List[PrintingModel]

def build_prompt(req: PrintingRequest) -> str:
    lines: List[str] = []

    lines.append(
        "Estimate printing and production costs accurately for each request.\n"
        "Use per-page pricing for printing, per-item pricing for production items and materials.\n"
        "Consider location-based pricing adjustments for remote locations.\n"
        "Include delivery costs if requested, otherwise price at $0.\n"
        "Round all USD amounts to whole dollars."
    )

    lines.append("\nRequests:\n")
    for i, p in enumerate(req.printing_data, start=1):
        lines.extend([
            f"Request {i}:",
            f"- Location: {p.location}",
        ])
        
        # Only include items with non-zero quantities
        printing_items = [
            ("B/W Single sided pages", p.bw_single_sided),
            ("B/W Double sided pages", p.bw_double_sided),
            ("Color Single sided pages", p.color_single_sided),
            ("Color Double sided pages", p.color_double_sided),
        ]
        
        production_items = [
            ("Certificates/Card Stock", p.certificate_card_stock),
            ("Simple Frames", p.simple_frame),
            ("Name Tags (Cardstock) w/ Lanyard", p.name_tag_cardstock_with_lanyard),
            ("Table Tents (Cardstock)", p.table_tent_cardstock),
        ]
        
        materials_items = [
            ("Binding - Spiral bound w/ Dividers", p.binding_spiral_bound_with_dividers),
            ("Binding - 3-Ring Binder w/ Dividers", p.binding_3ring_binder_with_dividers),
        ]
        
        # Add printing items
        for item_name, quantity in printing_items:
            if quantity > 0:
                lines.append(f"- {item_name}: {quantity}")
        
        # Add production items
        for item_name, quantity in production_items:
            if quantity > 0:
                lines.append(f"- {item_name}: {quantity}")
        
        # Add materials items
        for item_name, quantity in materials_items:
            if quantity > 0:
                lines.append(f"- {item_name}: {quantity}")
        
        lines.append(f"- Delivery: {'yes' if p.delivery else 'no'}")
        lines.append("")

    lines.append(
        "For each request, return JSON that matches the expected schema, followed by a brief explanation. "
        "Show simple math for each line (rate × quantity). Ensure the total equals the sum of "
        "printing costs, production costs, materials costs, and delivery fees."
    )

    return "\n".join(lines)


class PrintingResponseModel(BaseModel):
    res: list[LLMResponseModel]

def get_printing_estimate(req: PrintingRequest) -> List[LLMResponseModel]:
    system_msg = (
        "You are a careful printing and production cost estimator. "
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
        text_format=PrintingResponseModel,
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