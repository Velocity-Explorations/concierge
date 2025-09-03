from fast_flights import Flight, FlightData, Passengers, Result, get_flights, create_filter, get_flights_from_filter
from typing import List, Literal, Optional

from pydantic import BaseModel, Field
from typing import Any


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


class OneWayFlight(BaseModel):
    """
    One-way flight request.
    """
    
    kind: Literal["one-way"] = "one-way"
    date: str = Field(..., description="Date (e.g., '2025-08-14')")
    from_airport: str = Field(..., min_length=3, max_length=3, description="IATA code")
    to_airport: str = Field(..., min_length=3, max_length=3, description="IATA code")
    max_stops: Optional[int] = Field(default=None, ge=0)
    seat: Literal["economy", "premium-economy", "business", "first"]
    passengers: PassengerModel
    fetch_mode: Literal["common", "fallback", "force-fallback", "local"] = "common"


class RoundTripFlight(BaseModel):
    """
    Round-trip flight request.
    """
    
    kind: Literal["round-trip"] = "round-trip"
    outbound_date: str = Field(..., description="Departure date (e.g., '2025-08-14')")
    return_date: str = Field(..., description="Return date (e.g., '2025-08-14')")
    from_airport: str = Field(..., min_length=3, max_length=3, description="IATA code")
    to_airport: str = Field(..., min_length=3, max_length=3, description="IATA code")
    max_stops: Optional[int] = Field(default=None, ge=0)
    seat: Literal["economy", "premium-economy", "business", "first"]
    passengers: PassengerModel
    fetch_mode: Literal["common", "fallback", "force-fallback", "local"] = "common"
    max_combinations: int = Field(default=20, ge=1, description="Maximum round-trip combinations to generate")


class RoundTripOption(BaseModel):
    """
    Represents a complete round-trip flight option with both outbound and return flights.
    """
    
    outbound_flight: Flight
    return_flight: Flight
    total_price: float

class FlightRequest(BaseModel):
    flights: List[OneWayFlight | RoundTripFlight]


def get_complete_roundtrip_flights(
    outbound_date: str,
    return_date: str, 
    from_airport: str,
    to_airport: str,
    adults: int = 1,
    children: int = 0,
    infants_in_seat: int = 0,
    infants_on_lap: int = 0,
    seat_class: Literal["economy", "premium-economy", "business", "first"] = "economy",
    max_stops: Optional[int] = None,
    fetch_mode: Literal["common", "fallback", "force-fallback", "local"] = "common",
    max_combinations: int = 20
) -> List[RoundTripOption]:
    """
    Get complete round-trip flights by making separate outbound and return requests.
    
    Args:
        outbound_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format  
        from_airport: Origin airport code
        to_airport: Destination airport code
        adults: Number of adult passengers
        children: Number of child passengers (2-11 years)
        infants_in_seat: Number of infants with their own seat
        infants_on_lap: Number of infants on lap
        seat_class: Seat class (economy, premium-economy, business, first)
        max_stops: Maximum number of stops
        fetch_mode: Fetch mode (common, fallback, force-fallback, local)
        max_combinations: Maximum number of round-trip combinations to generate
        
    Returns:
        List of RoundTripOption objects with both outbound and return flights
    """
    
    passengers = Passengers(
        adults=adults,
        children=children,
        infants_in_seat=infants_in_seat,
        infants_on_lap=infants_on_lap
    )

    # Get outbound flights (one-way)
    print("Fetching outbound flights...")
    outbound_filter = create_filter(
        flight_data=[
            FlightData(
                date=outbound_date,
                from_airport=from_airport,
                to_airport=to_airport,
                max_stops=max_stops
            )
        ],
        trip="one-way",
        passengers=passengers,
        seat=seat_class,
        max_stops=max_stops
    )
    
    outbound_result = get_flights_from_filter(outbound_filter, mode=fetch_mode)
    if not outbound_result or not isinstance(outbound_result, Result):
        print("No outbound flights found")
        return []

    # Get return flights (one-way) 
    print("Fetching return flights...")
    return_filter = create_filter(
        flight_data=[
            FlightData(
                date=return_date,
                from_airport=to_airport,
                to_airport=from_airport,
                max_stops=max_stops
            )
        ],
        trip="one-way",
        passengers=passengers,
        seat=seat_class,
        max_stops=max_stops
    )
    
    return_result = get_flights_from_filter(return_filter, mode=fetch_mode)
    if not return_result or not isinstance(return_result, Result):
        print("No return flights found")
        return []

    print(f"Found {len(outbound_result.flights)} outbound and {len(return_result.flights)} return flights")
    
    # Generate round-trip combinations
    combinations = []
    for i, outbound in enumerate(outbound_result.flights[:max_combinations]):
        for j, return_flight in enumerate(return_result.flights[:max_combinations]):
            if len(combinations) >= max_combinations:
                break
                
            total_price = float(outbound.price[1:]) + float(return_flight.price[1:])
            
            combinations.append(RoundTripOption(
                outbound_flight=outbound,
                return_flight=return_flight,
                total_price=total_price
            ))
    
    # Sort by total price
    combinations.sort(key=lambda x: x.total_price)
    return combinations[:max_combinations]


def fetch_flights(req: FlightRequest) -> list[Result | List[RoundTripOption]]:
    results = []
    
    for flight in req.flights:
        try:
            passengers_obj = Passengers(
                adults=flight.passengers.adults,
                children=flight.passengers.children,
                infants_in_seat=flight.passengers.infants_in_seat,
                infants_on_lap=flight.passengers.infants_on_lap,
            )

            if flight.kind == "one-way":
                result = get_flights(
                    flight_data=[
                        FlightData(
                            date=flight.date,
                            from_airport=flight.from_airport,
                            to_airport=flight.to_airport,
                            max_stops=flight.max_stops,
                        )
                    ],
                    trip="one-way",
                    seat=flight.seat,
                    passengers=passengers_obj,
                    fetch_mode=flight.fetch_mode,
                )
                results.append(result)
                
            elif flight.kind == "round-trip":
                round_trip_options = get_complete_roundtrip_flights(
                    outbound_date=flight.outbound_date,
                    return_date=flight.return_date,
                    from_airport=flight.from_airport,
                    to_airport=flight.to_airport,
                    adults=flight.passengers.adults,
                    children=flight.passengers.children,
                    infants_in_seat=flight.passengers.infants_in_seat,
                    infants_on_lap=flight.passengers.infants_on_lap,
                    seat_class=flight.seat,
                    max_stops=flight.max_stops,
                    fetch_mode=flight.fetch_mode,
                    max_combinations=flight.max_combinations
                )
                results.append(round_trip_options)

        except Exception as e:
            print(f"Error processing flight {flight}: {e}")
            if flight.kind == "one-way":
                results.append(Result(current_price="high", flights=[]))
            else:
                results.append([])

    return results
