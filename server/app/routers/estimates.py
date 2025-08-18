from fastapi import APIRouter
from fast_flights import FlightData, Passengers, get_flights
from server.app.fetchers.flights import FlightRequest, fetch_flights
from server.app.fetchers.per_diem import PerDiemRequest, get_per_diem_estimate

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
 