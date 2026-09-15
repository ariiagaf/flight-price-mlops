import requests
import streamlit as st


st.set_page_config(
    page_title="Flight Price Prediction",
    page_icon="✈️",
)

st.title("Flight Price Prediction")

airline = st.selectbox(
    "Airline",
    ["SpiceJet", "AirAsia", "Vistara", "GO_FIRST", "Indigo", "Air_India"],
)

source_city = st.selectbox(
    "Source city",
    ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"],
)

destination_city = st.selectbox(
    "Destination city",
    ["Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai", "Delhi"],
)

departure_time = st.selectbox(
    "Departure time",
    ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"],
)

arrival_time = st.selectbox(
    "Arrival time",
    ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"],
)

stops = st.selectbox(
    "Stops",
    ["zero", "one", "two_or_more"],
)

flight_class = st.selectbox(
    "Class",
    ["Economy", "Business"],
)

duration = st.number_input(
    "Duration (hours)",
    min_value=0.5,
    max_value=50.0,
    value=2.5,
    step=0.1,
)

days_left = st.number_input(
    "Days left before departure",
    min_value=1,
    max_value=49,
    value=10,
    step=1,
)


if st.button("Predict price"):
    data = {
        "airline": airline,
        "source_city": source_city,
        "departure_time": departure_time,
        "stops": stops,
        "arrival_time": arrival_time,
        "destination_city": destination_city,
        "flight_class": flight_class,
        "duration": duration,
        "days_left": days_left,
    }

    try:
        response = requests.post(
            "http://api:8000/predict",
            json=data,
        )

        response.raise_for_status()

        result = response.json()

        predicted_price = result["predicted_price"]

        st.success(
            f"Predicted price: {predicted_price:.2f}"
        )

    except requests.exceptions.RequestException as error:
        st.error(
            f"Could not connect to the prediction API: {error}"
        )