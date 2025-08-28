from app.fetchers.openai import client
from typing import List, Literal
from pydantic import BaseModel

from app.fetchers._types import LLMResponseModel


# Breakout room with setup option
class BreakoutRoomModel(BaseModel):
    quantity: int = 0
    setup: bool = False

# Coffee services
class CoffeeBreakModel(BaseModel):
    am_break_per_person: int = 0
    pm_break_per_person: int = 0
    coffee_tea_station_all_day_per_person: int = 0

# A/V Package
class AVPackageModel(BaseModel):
    quantity: int = 0
    includes_description: str = ""

# Individual A/V Equipment
class AVEquipmentModel(BaseModel):
    projector: int = 0
    sound_system: int = 0
    screen: int = 0
    tabletop_microphone: int = 0
    laptop: int = 0
    power_strip_extension_cords: int = 0
    printer: int = 0

# Miscellaneous services
class MiscModel(BaseModel):
    setup_cleanup: bool = False
    onsite_support: bool = False
    delivery: bool = False
    meeting_supplies: bool = False
    other: bool = False
    other_description: str = ""

# Main venue model with venue type selection
class VenueModel(BaseModel):
    location: str
    duration_hours: int
    pax: int  # Number of people
    
    # Venue type selection
    venue_type: Literal["venue_package", "conference_room_package", "conference_room"]
    
    breakout_room: BreakoutRoomModel
    coffee_breaks: CoffeeBreakModel
    av_package: AVPackageModel
    av_equipment: AVEquipmentModel
    misc: MiscModel

class VenueRequest(BaseModel):
    venue_data: List[VenueModel]

def build_prompt(req: VenueRequest) -> str:
    lines: List[str] = []

    lines.append(
        "Estimate venue rental and event service costs accurately for each request.\n"
        "Use hourly rates for venue packages, per-person rates for coffee services, and item rates for A/V equipment.\n"
        "Consider location-based pricing adjustments for different cities and venues.\n"
        "If an item quantity is 0 or service isn't requested, price it at $0.\n"
        "Round all USD amounts to whole dollars."
    )

    lines.append("\nRequests:\n")
    for i, v in enumerate(req.venue_data, start=1):
        lines.extend([
            f"Request {i}:",
            f"- Location: {v.location}",
            f"- Duration: {v.duration_hours} hours",
            f"- PAX (people): {v.pax}",
        ])
        
        # Venue type
        if v.venue_type == "venue_package":
            lines.append("- Venue Package (room, water, A/V, catering)")
        elif v.venue_type == "conference_room_package":
            lines.append("- Conference Room Package (room, water, A/V, coffee breaks)")
        elif v.venue_type == "conference_room":
            lines.append("- Conference Room (bottled water and pen/notepad only)")
        
        # Breakout room
        if v.breakout_room.quantity > 0:
            setup_text = " with setup" if v.breakout_room.setup else ""
            lines.append(f"- Breakout Room: {v.breakout_room.quantity}{setup_text}")
        
        # Coffee services
        if v.coffee_breaks.am_break_per_person > 0:
            lines.append(f"- AM Coffee Break (light) per person: {v.coffee_breaks.am_break_per_person}")
        
        if v.coffee_breaks.pm_break_per_person > 0:
            lines.append(f"- PM Coffee Break (light) per person: {v.coffee_breaks.pm_break_per_person}")
        
        if v.coffee_breaks.coffee_tea_station_all_day_per_person > 0:
            lines.append(f"- Coffee and Tea Station All Day per person: {v.coffee_breaks.coffee_tea_station_all_day_per_person}")
        
        # A/V Package
        if v.av_package.quantity > 0:
            lines.append(f"- A/V Package: {v.av_package.quantity}")
            if v.av_package.includes_description:
                lines.append(f"  - Package includes: {v.av_package.includes_description}")
        
        # A/V Equipment
        av_items = [
            ("Projector", v.av_equipment.projector),
            ("Sound System", v.av_equipment.sound_system),
            ("Screen", v.av_equipment.screen),
            ("Tabletop Microphone", v.av_equipment.tabletop_microphone),
            ("Laptop", v.av_equipment.laptop),
            ("Power Strip/Extension Cords", v.av_equipment.power_strip_extension_cords),
            ("Printer", v.av_equipment.printer),
        ]
        
        for item_name, quantity in av_items:
            if quantity > 0:
                lines.append(f"- A/V {item_name}: {quantity}")
        
        # Misc services
        services = []
        if v.misc.setup_cleanup:
            services.append("Setup/Cleanup")
        if v.misc.onsite_support:
            services.append("Onsite Support")
        if v.misc.delivery:
            services.append("Delivery")
        if v.misc.meeting_supplies:
            services.append("Meeting Supplies")
        if v.misc.other and v.misc.other_description:
            services.append(f"Other: {v.misc.other_description}")
        
        for service in services:
            lines.append(f"- {service}: yes")
        
        lines.append("")

    lines.append(
        "For each request, return JSON that matches the expected schema, followed by a brief explanation. "
        "Show simple math for each line (rate × quantity × duration or per person). Ensure the total equals the sum of "
        "venue rental, catering, A/V equipment, and service costs."
    )

    return "\n".join(lines)


class VenueResponseModel(BaseModel):
    res: list[LLMResponseModel]

def get_venue_estimate(req: VenueRequest) -> List[LLMResponseModel]:
    system_msg = (
        "You are a careful venue and event service cost estimator. "
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
        text_format=VenueResponseModel,
        temperature=0.2,
        top_p=1,
        max_output_tokens=1200,
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