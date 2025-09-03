from fast_flights import FlightData, Passengers, Result, get_flights, search_airport
from typing import List, Literal
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from rapidfuzz import process
import pandas as pd
import math


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
    from_country: str = Field(..., min_length=2, max_length=100, description="Country Name")
    to_country: str = Field(..., min_length=2, max_length=100, description="Country Name")
    from_city: str = Field(..., min_length=3, max_length=100, description="City Name")
    to_city: str = Field(..., min_length=3, max_length=100, description="City Name")
    max_stops: int | None = Field(default=None, ge=0)

    trip: Literal["round-trip", "one-way", "multi-city"]
    seat: Literal["economy", "premium-economy", "business", "first"]
    passenger: PassengerModel
    fetch_mode: Literal["common", "fallback", "force-fallback", "local"]


class FlightRequest(BaseModel):
    flight_data: List[FlightDataModel]

AIRPORTS_FILE_PATH = Path(__file__).parent / "airports.csv"
CITIES_FILE_PATH = Path(__file__).parent / "cities.csv"


airports = pd.read_csv(AIRPORTS_FILE_PATH)
cities = pd.read_csv(CITIES_FILE_PATH)


def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def parse_point(point_str):
    # Example: "POINT (37.7749 -122.4194)"
    point_str = point_str.replace("POINT (", "").replace(")", "")
    lng_str, lat_str = point_str.split()
    return float(lat_str), float(lng_str)

def fuzzy_search(df: pd.DataFrame, column: str, query: str, limit: int = 5, threshold: int = 80):
    choices = df[column].astype(str).tolist()
    results = process.extract(query, choices, limit=limit, score_cutoff=threshold)
    matched_indices = [idx for _, _, idx in results]
    return df.iloc[matched_indices]

def get_city_row(cities_df, country, city):
    country_matches = fuzzy_search(cities_df, "country", country, limit=5000)
    city_matches = fuzzy_search(country_matches, "city", city, threshold=75)
    if city_matches.empty:
        raise ValueError("City not found")
    return city_matches.iloc[0]

def get_airports_in_country(airports_df, country_id):
    return airports_df[airports_df["country_id"] == country_id]

def get_nearby_airports(airports_df, city_lat, city_lng, max_distance=50):
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

def get_airport_code(country: str, city: str, max_distance: int = 50):
    city_row = get_city_row(cities, country.lower(), city.lower())
    country_id = city_row["iso2"]
    city_lat = float(city_row["lat"])
    city_lng = float(city_row["lng"])
    possible_airports = get_airports_in_country(airports, country_id)
    nearby_airports = get_nearby_airports(possible_airports, city_lat, city_lng, max_distance)
    return nearby_airports["code"].tolist()

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

            from_airports= get_airport_code(fd.from_country, fd.from_city, 20)
            to_airports= get_airport_code(fd.to_country, fd.to_city, 20)

            for departure in from_airports:
                for arrival in to_airports:
                    try:
                        results.append(
                            get_flights(
                                flight_data=[
                                    FlightData(
                                        date=fd.date,
                                        from_airport=departure,
                                        to_airport=arrival,
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
                        pass

        except Exception as e:
            print(f"Error processing flight data {fd}: {e}")
            results.append(Result(current_price="high", flights=[]))

    return results




