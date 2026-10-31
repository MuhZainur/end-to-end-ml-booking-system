import streamlit as st
import requests
import json
import pandas as pd

# Set Page Config
st.set_page_config(
    page_title="BA Booking Predictor",
    page_icon="✈️",
    layout="centered"
)

# Custom CSS for aesthetics (British Airways colors)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #002244;
        color: white;
        border-radius: 5px;
        width: 100%;
        height: 50px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #d71920;
        color: white;
    }
    h1 {
        color: #002244;
        text-align: center;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        color: white;
    }
    .success {
        background-color: #28a745;
    }
    .failure {
        background-color: #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.image("https://upload.wikimedia.org/wikipedia/en/thumb/9/9b/British_Airways_Logo.svg/1200px-British_Airways_Logo.svg.png", width=300)
st.title("Customer Booking Predictor")
st.markdown("Use this tool to predict if a customer will complete their flight booking based on their search behavior.")

st.divider()

# Input Form
with st.form("prediction_form"):
    st.header("📋 Customer Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        route = st.text_input("Route Origin-Dest (e.g., AKLDEL)", value="AKLDEL", help="IATA Codes for Origin and Destination concatenated")
        booking_origin = st.text_input("Booking Origin (Country)", value="New Zealand")
        flight_day = st.selectbox("Flight Day", ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        sales_channel = st.selectbox("Sales Channel", ['Internet', 'Mobile'])
        trip_type = st.selectbox("Trip Type", ['RoundTrip', 'OneWay', 'CircleTrip'])
        flight_duration = st.number_input("Flight Duration (Hours)", min_value=0.0, max_value=24.0, value=8.5, step=0.5)

    with col2:
        num_passengers = st.number_input("Number of Passengers", min_value=1, max_value=10, value=1)
        purchase_lead = st.number_input("Purchase Lead (Days)", min_value=0, max_value=800, value=30, help="Days between booking and travel")
        length_of_stay = st.number_input("Length of Stay (Days)", min_value=0, max_value=365, value=5)
        flight_hour = st.slider("Flight Departure Hour", 0, 23, 12)
        
        st.write("---")
        st.write("**Extra Services**")
        wants_extra_baggage = st.checkbox("Wants Extra Baggage", value=True)
        wants_preferred_seat = st.checkbox("Wants Preferred Seat", value=False)
        wants_in_flight_meals = st.checkbox("Wants In-Flight Meals", value=True)
    
    # Submit Button
    submit_button = st.form_submit_button(label="🔮 Predict Booking Probability")

# Backend API URL (Ensure this matches your FastAPI Port)
API_URL = "http://127.0.0.1:8000/predict"

if submit_button:
    # Prepare payload
    payload = {
        "num_passengers": int(num_passengers),
        "sales_channel": sales_channel,
        "trip_type": trip_type,
        "purchase_lead": int(purchase_lead),
        "length_of_stay": int(length_of_stay),
        "flight_hour": int(flight_hour),
        "flight_day": flight_day,
        "route": route.upper(),
        "booking_origin": booking_origin,
        "wants_extra_baggage": 1 if wants_extra_baggage else 0,
        "wants_preferred_seat": 1 if wants_preferred_seat else 0,
        "wants_in_flight_meals": 1 if wants_in_flight_meals else 0,
        "flight_duration": float(flight_duration)
    }

    try:
        with st.spinner("Analyzing customer profile..."):
            response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            pred = result['prediction'] # 1 or 0
            prob = result['confidence_score'] # 0.0 to 1.0
            
            # Display Results
            st.markdown("### 📊 Prediction Result")
            
            if pred == 1:
                st.markdown(f"""
                <div class="prediction-box success">
                    <h2>✅ Booking Likely</h2>
                    <p>Confidence: <strong>{prob*100:.1f}%</strong></p>
                    <p>{result['message']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                 st.markdown(f"""
                <div class="prediction-box failure">
                    <h2>❌ Booking Unlikely</h2>
                    <p>Confidence of Booking: <strong>{prob*100:.1f}%</strong></p>
                    <p>{result['message']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # JSON Debug Expander
            with st.expander("View Analysis Details (JSON)"):
                st.json(result)
                st.write("Input Payload sent:")
                st.json(payload)
                
        else:
            st.error(f"Server Error: {response.status_code}")
            st.write(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("🚨 Connection Error! Is the Backend Server (FastAPI) running? Please check your terminal.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
