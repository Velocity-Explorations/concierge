from fastapi import APIRouter, UploadFile, File, HTTPException
from app.fetchers.flights.flights import FlightRequest, fetch_flights
from app.fetchers.per_diem.fetcher import PerDiemRequest, get_per_diem_estimate
from app.fetchers.translations._types import TranslationRequest
from app.fetchers.translations.fetcher import fetch_translations, load_historical_data
from app.fetchers.catering import CateringRequest, get_catering_estimate
from app.fetchers.equipment import EquipmentRequest, get_equipment_estimate
from app.fetchers.printing import PrintingRequest, get_printing_estimate
from app.fetchers.venue import VenueRequest, get_venue_estimate
from app.fetchers.visa import VisaRequest, get_visa_estimate
from app.fetchers.ground_transport import GroundTransportRequest, get_ground_transport_estimate

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

@router.post("/translations/update")
async def update_translation_data(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    csv_content = await file.read()
    csv_str = csv_content.decode('utf-8')
    
    return load_historical_data(csv_str)

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

@router.post("/venue")
async def find_venue(req: VenueRequest):
    return get_venue_estimate(
        req
    )

@router.post("/visa")
async def find_visa(req: VisaRequest):
    return get_visa_estimate(
        req
    )


@router.post("/ground-transport")
async def find_ground_transport(req: GroundTransportRequest):
    return get_ground_transport_estimate(
        req
    )