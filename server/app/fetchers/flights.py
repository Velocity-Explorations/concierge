from fast_flights import FlightData, Passengers, Result, get_flights
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class PassengerModel(BaseModel):
    """
    Pydantic version of Passengers.
    """

    adults: int = Field(..., ge=1, description="Number of adults")
    children: int = Field(default=0, ge=0, description="Number of children")
    infants_in_seat: int = Field(
        default=0, ge=0, description="Number of infants in seats"
    )
    infants_on_lap: int = Field(
        default=0, ge=0, description="Number of infants on laps"
    )


class FlightDataModel(BaseModel):
    """
    Pydantic version of FlightData.

    - Accepts Airport enum *or* string for from/to fields.
    - Serializes out as uppercase IATA strings.
    """

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    date: str = Field(..., description="Date (e.g., '2025-08-14')")
    from_airport: str = Field(..., min_length=3, max_length=3, description="IATA code")
    to_airport: str = Field(..., min_length=3, max_length=3, description="IATA code")
    max_stops: int | None = Field(default=None, ge=0)

    trip: Literal["round-trip", "one-way", "multi-city"]
    seat: Literal["economy", "premium-economy", "business", "first"]
    passenger: PassengerModel
    fetch_mode: Literal["common", "fallback", "force-fallback", "local"]


class FlightRequest(BaseModel):
    flight_data: List[FlightDataModel]


def fetch_flights(req: FlightRequest) -> list[Result]:

    results: list[Result] = []

    for fd in req.flight_data:
        try:
            passengers_obj = Passengers(
                adults=fd.passenger.adults,
                children=fd.passenger.children,
                infants_in_seat=fd.passenger.infants_in_seat,
                infants_on_lap=fd.passenger.infants_on_lap,
            )

            results.append(
                get_flights(
                    flight_data=[
                        FlightData(
                            date=fd.date,
                            from_airport=fd.from_airport,
                            to_airport=fd.to_airport,
                            max_stops=fd.max_stops,
                        )
                    ],
                    trip=fd.trip,
                    seat=fd.seat,
                    passengers=passengers_obj,
                    fetch_mode=fd.fetch_mode,
                )
            )

        except Exception as e:
            print(f"Error processing flight data {fd}: {e}")
            results.append(Result(current_price="high", flights=[]))

    return results
