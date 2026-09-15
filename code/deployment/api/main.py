from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = Path("/app/models/flight_price_model.pkl")

if not MODEL_PATH.exists():
    MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "flight_price_model.pkl"

model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Flight Price Prediction API"
)

class FlightInput(BaseModel):
    airline: str
    source_city: str
    departure_time: str
    stops: str
    arrival_time: str
    destination_city: str
    flight_class: str
    duration: float
    days_left: int


@app.get("/")
def home():
    return {
        "message": "Flight Price Prediction API is running"
    }


@app.post("/predict")
def predict(data: FlightInput):
    input_data = pd.DataFrame(
        [
            {
                "airline": data.airline,
                "source_city": data.source_city,
                "departure_time": data.departure_time,
                "stops": data.stops,
                "arrival_time": data.arrival_time,
                "destination_city": data.destination_city,
                "class": data.flight_class,
                "duration": data.duration,
                "days_left": data.days_left,
            }
        ]
    )

    prediction = model.predict(input_data)[0]
    prediction = max(prediction, 1105)

    return {
        "predicted_price": round(float(prediction), 2)
    }