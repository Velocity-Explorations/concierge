from fast_flights import Flight, FlightData, Passengers, Result, get_flights, create_filter, get_flights_from_filter
from typing import List, Literal, Optional
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from concurrent.futures import ThreadPoolExecutor, as_completed
from rapidfuzz import process
import pandas as pd
import math
import statistics

# --- Models ---



class PassengerModel(BaseModel):
    adults: int = Field(..., ge=1, description="Number of adults")
    children: int = Field(default=0, ge=0, description="Number of children")
    infants_in_seat: int = Field(default=0, ge=0, description="Number of infants in seats")
    infants_on_lap: int = Field(default=0, ge=0, description="Number of infants on laps")

class OneWayFlight(BaseModel):
    kind: Literal["one-way"] = "one-way"
    date: str = Field(..., description="Date (e.g., '2025-08-14')")
    from_country: str = Field(..., min_length=2, max_length=100, description="Country Name")
    to_country: str = Field(..., min_length=2, max_length=100, description="Country Name")
    from_city: str = Field(..., min_length=3, max_length=100, description="City Name")
    to_city: str = Field(..., min_length=3, max_length=100, description="City Name")
    max_stops: int = Field(default=0, ge=0)
    seat: Literal["economy", "premium-economy", "business", "first"]
    passengers: PassengerModel
    fetch_mode: Literal["common", "fallback", "force-fallback", "local"] = "common"

class RoundTripFlight(BaseModel):
    kind: Literal["round-trip"] = "round-trip"
    outbound_date: str = Field(..., description="Departure date (e.g., '2025-08-14')")
    return_date: str = Field(..., description="Return date (e.g., '2025-08-14')")
    from_country: str = Field(..., min_length=2, max_length=100, description="Country Name")
    to_country: str = Field(..., min_length=2, max_length=100, description="Country Name")
    from_city: str = Field(..., min_length=3, max_length=100, description="City Name")
    to_city: str = Field(..., min_length=3, max_length=100, description="City Name")
    max_stops: int = Field(default=0, ge=0)
    seat: Literal["economy", "premium-economy", "business", "first"]
    passengers: PassengerModel
    fetch_mode: Literal["common", "fallback", "force-fallback", "local"] = "common"
    max_combinations: int = Field(default=20, ge=1, description="Maximum round-trip combinations to generate")

class RoundTripOption(BaseModel):
    outbound_flight: Flight
    return_flight: Flight
    total_price: float
    outbound_flight_from_airport: str
    outbound_flight_to_airport: str
    return_flight_from_airport: str
    return_flight_to_airport: str


class OneWayOption(BaseModel):
    flight: Flight
    total_price: float
    from_airport: str
    to_airport: str


class FlightRequest(BaseModel):
    flights: List[OneWayFlight | RoundTripFlight]

# --- Data Loading ---

AIRPORTS_FILE_PATH = Path(__file__).parent / "airports.csv"
CITIES_FILE_PATH = Path(__file__).parent / "cities.csv"

airports: pd.DataFrame = pd.read_csv(AIRPORTS_FILE_PATH)
cities: pd.DataFrame = pd.read_csv(CITIES_FILE_PATH)

# --- Utility Functions ---

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 3958.8  # Earth radius in miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def parse_point(point_str: str) -> tuple[float, float]:
    # Example: "POINT (37.7749 -122.4194)"
    point_str = point_str.replace("POINT (", "").replace(")", "")
    lng_str, lat_str = point_str.split()
    return float(lat_str), float(lng_str)

def fuzzy_search(df: pd.DataFrame, column: str, query: str, limit: int = 5, threshold: int = 80) -> pd.DataFrame:
    choices = df[column].astype(str).tolist()
    results = process.extract(query, choices, limit=limit, score_cutoff=threshold)
    matched_indices = [idx for _, _, idx in results]
    return df.iloc[matched_indices]

def get_city_row(cities_df: pd.DataFrame, country: str, city: str) -> pd.DataFrame:
    country_matches = fuzzy_search(cities_df, "country", country, limit=5000)
    city_matches = fuzzy_search(country_matches, "city", city, threshold=75)
    if city_matches.empty:
        raise ValueError("City not found")
    return city_matches.iloc[0]

def get_airports_in_country(airports_df: pd.DataFrame, country_id: str) -> pd.DataFrame:
    return airports_df[airports_df["country_id"] == country_id]

def get_nearby_airports(airports_df: pd.DataFrame, city_lat: float, city_lng: float, max_distance: int=50) -> pd.DataFrame:
    nearby = []
    for idx, row in airports_df.iterrows():
        try:
            airport_lat, airport_lng = parse_point(row["location"])
            distance = haversine(city_lat, city_lng, airport_lat, airport_lng)
            if distance <= max_distance:
                nearby.append(row)
        except Exception:
            continue
    return pd.DataFrame(nearby)

def get_airport_codes(country: str, city: str, max_distance: int = 50) -> List[str]:
    city_row = get_city_row(cities, country.lower(), city.lower())
    country_id = city_row["iso2"]
    city_lat = float(city_row["lat"])
    city_lng = float(city_row["lng"])
    possible_airports = get_airports_in_country(airports, country_id)
    nearby_airports = get_nearby_airports(possible_airports, city_lat, city_lng, max_distance)
    return nearby_airports["code"].tolist()


def search_pair(departure: str, arrival: str, date: str, seat: str, passengers: Passengers, max_stops: int, fetch_mode: str, retry_count: int = 2) -> List | Result:
    """
    Search for flights between airport pairs with retry logic.
    """
    for attempt in range(retry_count):
        try:
            result = get_flights(
                flight_data=[
                    FlightData(
                        date=date,
                        from_airport=departure,
                        to_airport=arrival,
                        max_stops=max_stops,
                    )
                ],
                trip="one-way",
                seat=seat,
                passengers=passengers,
                fetch_mode=fetch_mode if attempt == 0 else "fallback",  # Use fallback on retry
            )

            if isinstance(result, Result):
                for f in result.flights:  # limit per pair
                    f.from_airport = departure
                    f.to_airport = arrival
                result.flights = result.flights[:5]
                return result
        except Exception as e:
            if attempt == retry_count - 1:  # Last attempt
                print(f"Failed to fetch flights {departure}->{arrival} after {retry_count} attempts: {e}")
    return []

# --- Main Flight Logic ---

def get_complete_roundtrip_flights(
    outbound_date: str,
    return_date: str, 
    from_country: str,
    to_country: str,
    from_city: str,
    to_city: str,
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
    Get complete round-trip flights by making separate outbound and return requests,
    iterating over all airport pairs for both directions.
    """
    passengers = Passengers(
        adults=adults,
        children=children,
        infants_in_seat=infants_in_seat,
        infants_on_lap=infants_on_lap
    )

    # Get all possible airports for outbound and return directions
    from_airports = get_airport_codes(from_country, from_city, 20)
    to_airports = get_airport_codes(to_country, to_city, 20)

    outbound_flights = []
    return_flights = []

    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                search_pair, departure, arrival, outbound_date, seat_class, passengers, max_stops, fetch_mode
            )
            for departure in from_airports
            for arrival in to_airports
        ]
        for future in as_completed(futures):
            if isinstance(future.result(), Result):
                outbound_flights.extend(future.result().flights)
    
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                search_pair, departure, arrival, return_date, seat_class, passengers, max_stops, fetch_mode
            )
            for departure in to_airports
            for arrival in from_airports
        ]
        for future in as_completed(futures):
            if isinstance(future.result(), Result):
                return_flights.extend(future.result().flights)


    # Generate round-trip combinations
    combinations = []
    for outbound in outbound_flights[:max_combinations]:
        for return_flight in return_flights[:max_combinations]:
            if len(combinations) >= max_combinations:
                break
            try:
                total_price = float(outbound.price[1:]) + float(return_flight.price[1:])
            except Exception:
                total_price = 0.0
            combinations.append(RoundTripOption(
                outbound_flight=outbound,
                return_flight=return_flight,
                total_price=total_price,
                outbound_flight_from_airport=outbound.from_airport,
                outbound_flight_to_airport=outbound.to_airport,
                return_flight_from_airport=return_flight.from_airport,
                return_flight_to_airport=return_flight.to_airport,
            ))

    # Sort by price for median calculation
    combinations.sort(key=lambda x: x.total_price)
    
    # Select median-priced options rather than cheapest
    if len(combinations) > 5:
        # Find median index
        median_idx = len(combinations) // 2
        # Return options around the median
        start_idx = max(0, median_idx - max_combinations // 2)
        end_idx = min(len(combinations), start_idx + max_combinations)
        return combinations[start_idx:end_idx]
    return combinations[:max_combinations]

def fetch_flights(req: FlightRequest) -> list[OneWayOption | List[RoundTripOption]]:
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
                from_airports = get_airport_codes(flight.from_country, flight.from_city, 20)
                to_airports = get_airport_codes(flight.to_country, flight.to_city, 20)
                flight_results = []

                with ThreadPoolExecutor() as executor:
                    futures = [
                        executor.submit(search_pair, departure, arrival, flight.date, flight.seat, passengers_obj, flight.max_stops, flight.fetch_mode)
                        for departure in from_airports
                        for arrival in to_airports
                    ]
                    for future in as_completed(futures):
                        if isinstance(future.result(), Result):
                            flight_results.append(future.result())
                
                all_flights = []
                for flight_result in flight_results:
                    for flight in flight_result.flights:
                        all_flights.append(OneWayOption(
                            flight=flight,
                            total_price=float(flight.price[1:]) if flight.price else 0.0,
                            from_airport=flight.from_airport,
                            to_airport=flight.to_airport,
                        ))
                
                # Sort flights by price and select median-range options
                all_flights.sort(key=lambda x: x.total_price)
                if len(all_flights) > 10:
                    # Get median price
                    prices = [f.total_price for f in all_flights if f.total_price > 0]
                    if prices:
                        median_price = statistics.median(prices)
                        # Filter flights within 20% of median
                        median_flights = [
                            f for f in all_flights 
                            if median_price * 0.8 <= f.total_price <= median_price * 1.2
                        ]
                        # If we have median flights, use them; otherwise fall back to middle range
                        if median_flights:
                            results.extend(median_flights[:10])
                        else:
                            median_idx = len(all_flights) // 2
                            start_idx = max(0, median_idx - 5)
                            results.extend(all_flights[start_idx:start_idx + 10])
                    else:
                        results.extend(all_flights[:10])
                else:
                    results.extend(all_flights)

                


            elif flight.kind == "round-trip":
                round_trip_options = get_complete_roundtrip_flights(
                    outbound_date=flight.outbound_date,
                    return_date=flight.return_date,
                    from_country=flight.from_country,
                    to_country=flight.to_country,
                    from_city=flight.from_city,
                    to_city=flight.to_city,
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
            # Return empty result for failures instead of high price indicator
            if flight.kind == "one-way":
                results.append([])
            else:
                results.append([])

    return results
