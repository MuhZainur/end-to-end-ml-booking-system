from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from schemas import BookingRequest, BookingResponse
from model_loader import model_loader
import uvicorn
import os

app = FastAPI(
    title="BA Booking Prediction API",
    description="Real-time API for predicting customer booking likelihood using Random Forest.",
    version="1.0"
)

# CORS Configuration (Required for Frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Safe for public demo, restrict in enterprise)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """
    On startup, load the model from MLflow.
    """
    try:
        model_loader.load_model()
    except Exception as e:
        print("⚠️ Failed to load model on startup. Check MLflow connection.")

@app.get("/")
def home():
    return {"message": "British Airways Booking Prediction API is Running ✈️"}

@app.get("/health")
def health_check():
    if model_loader.model:
        return {"status": "healthy", "model_loaded": True}
    return {"status": "unhealthy", "model_loaded": False}

@app.post("/predict", response_model=BookingResponse)
def predict(request: BookingRequest):
    """
    Accepts booking details and returns prediction.
    """
    try:
        # Convert Pydantic object to DataFrame (Single row)
        data_dict = request.dict()
        # Ensure values are lists for DataFrame creation
        data = {k: [v] for k, v in data_dict.items()}
        df_input = pd.DataFrame(data)

        # Predict
        pred, prob = model_loader.predict(df_input)

        message = "Customer is LIKELY to book." if pred == 1 else "Customer is UNLIKELY to book."

        return BookingResponse(
            prediction=pred,
            confidence_score=prob,
            message=message
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
