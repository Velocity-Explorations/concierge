from fastapi import APIRouter
from app.routers._types import FlightRequest
from fast_flights import FlightData, Passengers, get_flights

router = APIRouter()


@router.post("/flights")
async def find_estimates(data: FlightRequest):

    return get_flights(
        flight_data=[
            FlightData(
                date=flight.date,
                from_airport=flight.from_airport,
                to_airport=flight.to_airport,
                max_stops=flight.max_stops
            )
            for flight in data.flight_data
        ],
        trip=data.trip,
        seat=data.seat,
        passengers=Passengers(
            adults=data.passenger.adults,
            children=data.passenger.children,
            infants_in_seat=data.passenger.infants_in_seat,
            infants_on_lap=data.passenger.infants_on_lap
        ),
        fetch_mode=data.fetch_mode,
    )
