from fastapi import APIRouter
from app.fetchers.flights import FlightRequest, fetch_flights
from app.fetchers.per_diem.fetcher import PerDiemRequest, get_per_diem_estimate
from app.fetchers.translations._types import TranslationRequest
from app.fetchers.translations.fetcher import fetch_translations
from app.fetchers.catering import CateringRequest, get_catering_estimate
from app.fetchers.equipment import EquipmentRequest, get_equipment_estimate
from app.fetchers.printing import PrintingRequest, get_printing_estimate

router = APIRouter()


@router.post("/flights")
async def find_estimates(req: FlightRequest):
    return fetch_flights(
        req
    )

@router.post("/per-diem")
async def find_meal_and_lodging(req: PerDiemRequest):
    return get_per_diem_estimate(
        req
    )
 
@router.post("/translations")
async def translate_texts(req: TranslationRequest):
    return fetch_translations(
        req
    )

@router.post("/catering")
async def find_catering(req: CateringRequest):
    return get_catering_estimate(
        req
    )

@router.post("/equipment")
async def find_equipment(req: EquipmentRequest):
    return get_equipment_estimate(
        req
    )

@router.post("/printing")
async def find_printing(req: PrintingRequest):
    return get_printing_estimate(
        req
    )