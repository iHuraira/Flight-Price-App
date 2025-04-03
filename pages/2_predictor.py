import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from random import randint

from src.components.data_model import FlightInputModel
from src.pipeline.predict_pipeline import PredictPipeline


# ------------------ UTILS ------------------

def format_duration(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}h {mins:02d}m"


def get_flight_code(flight_code_df, airline_name):
    available_codes = flight_code_df[flight_code_df['airline_name'] == airline_name]['flight_code'].tolist()
    return random.choice(available_codes) if available_codes else "UNKNOWN"


def generate_time_suggestions(duration_minutes):
    suggestions = []
    for _ in range(3):
        dep_hour = randint(4, 22)
        dep_min = randint(0, 59)
        dep_time = datetime.strptime(f"{dep_hour:02d}:{dep_min:02d}", "%H:%M")
        arr_time = dep_time + timedelta(minutes=duration_minutes)
        suggestions.append({
            "departure_time": dep_time.strftime("%H:%M"),
            "arrival_time": arr_time.strftime("%H:%M")
        })
    return suggestions


# ------------------ PAGE LOGIC ------------------

st.title("✈️ Estimated Flight Duration Finder")

# Data loading
duration_df = pd.read_csv("artifacts/Static/duration_summary.csv")
flight_code_df = pd.read_csv("artifacts/Static/flight_code.csv")

airline_map = {
    'Vistara': 'UK', 'Air India': 'AI', 'Indigo': '6E',
    'GO FIRST': 'G8', 'AirAsia': 'I5', 'SpiceJet': 'SG',
    'StarAir': 'S5', 'Trujet': '2T'
}

# Input selection
airline_name = st.selectbox("Select Airline", list(airline_map.keys()))
airline_code = airline_map[airline_name]
flight_code = get_flight_code(flight_code_df, airline_name)

flight_type = st.selectbox("Select Flight Type", ['economy', 'business'])
departure_city = st.selectbox("Select Departure City", duration_df['departure_city'].unique())

filtered_arrivals = duration_df[duration_df['departure_city'] == departure_city]['arrival_city'].unique()
arrival_city = st.selectbox("Select Arrival City", filtered_arrivals)

filtered_stops = duration_df[
    (duration_df['departure_city'] == departure_city) &
    (duration_df['arrival_city'] == arrival_city)
]['num_stops'].unique()
num_stops = st.selectbox("Select Number of Stops", sorted(filtered_stops))

# Duration lookup
match = duration_df[
    (duration_df['departure_city'] == departure_city) &
    (duration_df['arrival_city'] == arrival_city) &
    (duration_df['num_stops'] == num_stops)
]

if match.empty:
    st.warning("No data available for this combination.")

# Duration display
estimated_duration = round(match['avg_flight_duration_minutes'].values[0])
duration_formatted = format_duration(estimated_duration)
st.success(f"Estimated Flight Duration: {duration_formatted}")

# Time suggestion
st.subheader("🕒 Choose a Suggested Time Option")
current_selection = (departure_city, arrival_city, num_stops)

if st.session_state.get("last_selection") != current_selection:
    st.session_state.last_selection = current_selection
    st.session_state.time_suggestions = generate_time_suggestions(estimated_duration)

suggestions = st.session_state.time_suggestions
option_labels = [
    f"Option {i+1}: Dep {s['departure_time']} → Arr {s['arrival_time']}"
    for i, s in enumerate(suggestions)
]
selected_index = st.radio("Select a time slot:", list(range(3)), format_func=lambda x: option_labels[x])
selected_times = suggestions[selected_index]

# Final input model
input_model = FlightInputModel(
    airline_name=airline_name,
    airline_code=airline_code,
    flight_code=flight_code,
    flight_type=flight_type,
    departure_city=departure_city,
    arrival_city=arrival_city,
    stop_type=num_stops,
    flight_duration=duration_formatted,
    departure_time=selected_times['departure_time'],
    arrival_time=selected_times['arrival_time']
)

final_df = input_model.to_dataframe()

# Prediction
if st.button("🚀 Predict"):
    try:
        predictor = PredictPipeline()
        prediction = predictor.predict(final_df)
        st.success(f"🎯 Predicted Flight Price: ₹{round(prediction):,}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")