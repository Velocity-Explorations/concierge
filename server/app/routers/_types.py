from typing import List, Literal
from fast_flights import Passengers, Airport
from pydantic import BaseModel, Field, ConfigDict


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

class PassengerModel(BaseModel):
    """
    Pydantic version of Passengers.
    """
    adults: int = Field(..., ge=1, description="Number of adults")
    children: int = Field(default=0, ge=0, description="Number of children")
    infants_in_seat: int = Field(default=0, ge=0, description="Number of infants in seats")
    infants_on_lap: int = Field(default=0, ge=0, description="Number of infants on laps")

class FlightRequest(BaseModel):
    flight_data: List[FlightDataModel]
    trip: Literal["round-trip", "one-way", "multi-city"]
    seat: Literal["economy", "premium-economy", "business", "first"]
    passenger: PassengerModel
    fetch_mode: Literal["common", "fallback", "force-fallback", "local"]
