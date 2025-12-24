import requests
import json

# Sample payload based on schema
payload = {
    "num_passengers": 2,
    "sales_channel": "Internet",
    "trip_type": "RoundTrip",
    "purchase_lead": 20,
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

print("🚀 Sending Test Request to http://127.0.0.1:8000/predict ...")

try:
    response = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"❌ Could not connect to server: {e}")
    print("Make sure you run 'uvicorn main:app --reload' in the Backend directory first.")
