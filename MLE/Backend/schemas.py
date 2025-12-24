from pydantic import BaseModel, Field
from typing import Literal

class BookingRequest(BaseModel):
    num_passengers: int = Field(..., description="Number of passengers travelling", ge=1)
    sales_channel: Literal['Internet', 'Mobile'] = Field(..., description="Sales channel used")
    trip_type: Literal['RoundTrip', 'OneWay', 'CircleTrip'] = Field(..., description="Type of trip")
    purchase_lead: int = Field(..., description="Number of days between booking and travel", ge=0)
    length_of_stay: int = Field(..., description="Number of days spent at destination", ge=0)
    flight_hour: int = Field(..., description="Hour of flight departure", ge=0, le=23)
    flight_day: Literal['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] = Field(..., description="Day of flight departure")
    route: str = Field(..., description="Flight Route (e.g., AKLDEL)")
    booking_origin: str = Field(..., description="Country of booking origin")
    wants_extra_baggage: int = Field(..., description="1 if wanted extra baggage, else 0", ge=0, le=1)
    wants_preferred_seat: int = Field(..., description="1 if wanted preferred seat, else 0", ge=0, le=1)
    wants_in_flight_meals: int = Field(..., description="1 if wanted in-flight meals, else 0", ge=0, le=1)
    flight_duration: float = Field(..., description="Total duration of flight in hours", ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "num_passengers": 2,
                "sales_channel": "Internet",
                "trip_type": "RoundTrip",
                "purchase_lead": 45,
                "length_of_stay": 5,
                "flight_hour": 14,
                "flight_day": "Wed",
                "route": "AKLDEL",
                "booking_origin": "New Zealand",
                "wants_extra_baggage": 1,
                "wants_preferred_seat": 0,
                "wants_in_flight_meals": 1,
                "flight_duration": 8.5
            }
        }
    }

class BookingResponse(BaseModel):
    prediction: int = Field(..., description="1 = Booking Likely, 0 = Unlikely")
    confidence_score: float = Field(..., description="Probability of booking (0.0 to 1.0)")
    message: str = Field(..., description="Human-readable interpretation")
