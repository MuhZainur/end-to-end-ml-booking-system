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
    On startup, load the model (Local pkl with MLflow fallback).
    """
    try:
        model_loader.load_model()
    except Exception as e:
        print(f"⚠️ Failed to load model on startup: {e}")

@app.get("/")
def home():
    return {
        "message": "British Airways Booking Prediction API is Running",
        "docs": "/docs",
        "model_status": "Loaded" if model_loader.model else "Ready",
        "model_source": model_loader.model_source
    }

@app.get("/health")
def health_check():
    if not model_loader.model:
        model_loader.load_model()
    if model_loader.model:
        return {"status": "healthy", "model_loaded": True, "source": model_loader.model_source}
    return {"status": "online", "model_loaded": False, "mode": "heuristic_fallback"}

@app.post("/predict", response_model=BookingResponse)
def predict(request: BookingRequest):
    """
    Accepts booking details and returns prediction.
    """
    try:
        # Convert Pydantic object to DataFrame (Single row)
        data_dict = request.dict()
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
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
