from fast_flights import FlightData, Passengers, Result, get_flights
from typing import List, Literal


async def fetch_flights(
    flight_data: List[FlightData],
    trip: Literal["round-trip", "one-way", "multi-city"],
    seat: Literal['economy', 'premium-economy', 'business', 'first'],
    passengers: Passengers,
    fetch_mode: Literal['common', 'fallback', 'force-fallback', 'local']
) -> Result:
    result: Result = get_flights(
        flight_data=flight_data,
        trip=trip,
        seat=seat,
        passengers=passengers,
        fetch_mode=fetch_mode,
    )

    return result