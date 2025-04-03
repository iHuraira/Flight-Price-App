import sys
import os

import joblib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import random
import streamlit as st
import pandas as pd
from random import randint
from datetime import datetime, timedelta
from src.components.ml_components.data_preparation import DataPreparation

def format_duration(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}h {mins:02d}m"

airline_map = {
    'Vistara': 'UK',
    'Air India': 'AI',
    'Indigo': '6E',
    'GO FIRST': 'G8',
    'AirAsia': 'I5',
    'SpiceJet': 'SG',
    'StarAir': 'S5',
    'Trujet': '2T'
}


# Load your grouped duration data
duration_df = pd.read_csv("artifacts/Static/duration_summary.csv")
flight_code_df = pd.read_csv("artifacts/Static/flight_code.csv")

st.title("✈️ Estimated Flight Duration Finder")

airline_name = st.selectbox("Select Airline", list(airline_map.keys()))
airline_code = airline_map[airline_name]

# Filter all rows for selected airline
available_codes = flight_code_df[flight_code_df['airline_name'] == airline_name]['flight_code'].tolist()


flight_code_row = flight_code_df[flight_code_df['airline_name'] == airline_name]
flight_code = random.choice(available_codes) if available_codes else "UNKNOWN"

flight_type = st.selectbox("Select Flight Type", ['economy', 'business'])

# --- Step 1: City and stop selection ---
departure_city = st.selectbox("Select Departure City", duration_df['departure_city'].unique())

filtered_arrivals = duration_df[duration_df['departure_city'] == departure_city]['arrival_city'].unique()
arrival_city = st.selectbox("Select Arrival City", filtered_arrivals)

filtered_stops = duration_df[
    (duration_df['departure_city'] == departure_city) &
    (duration_df['arrival_city'] == arrival_city)
]['num_stops'].unique()
num_stops = st.selectbox("Select Number of Stops", sorted(filtered_stops))

# --- Step 2: Match and estimate duration ---
match = duration_df[
    (duration_df['departure_city'] == departure_city) &
    (duration_df['arrival_city'] == arrival_city) &
    (duration_df['num_stops'] == num_stops)
]

if not match.empty:
    estimated_duration = round(match['avg_flight_duration_minutes'].values[0])
    duration_formatted = format_duration(estimated_duration)
    st.success(f"Estimated Flight Duration: {duration_formatted}")


    st.subheader("🕒 Choose a Suggested Time Option")

    # Detect change and regenerate suggestions
    current_selection = (departure_city, arrival_city, num_stops)
    if st.session_state.get("last_selection") != current_selection:
        st.session_state.last_selection = current_selection
        # Regenerate suggestions
        suggestions = []
        for _ in range(3):
            dep_hour = randint(4, 22)
            dep_min = randint(0, 59)
            dep_time = datetime.strptime(f"{dep_hour:02d}:{dep_min:02d}", "%H:%M")
            arr_time = dep_time + timedelta(minutes=estimated_duration)
            suggestions.append({
                "departure_time": dep_time.strftime("%H:%M"),
                "arrival_time": arr_time.strftime("%H:%M")
            })
        st.session_state.time_suggestions = suggestions
    else:
        suggestions = st.session_state.time_suggestions


    # Create option labels for radio buttons
    option_labels = [
        f"Option {i+1}: Dep {s['departure_time']} → Arr {s['arrival_time']}"
        for i, s in enumerate(suggestions)
    ]

    selected_index = st.radio("Select a time slot:", list(range(3)), format_func=lambda x: option_labels[x])

    selected_times = suggestions[selected_index]
    
    prepared_data = DataPreparation()

    # --- Step 3: Show final DataFrame ---
    final_df = pd.DataFrame([{
        "airline_name": airline_name,
        "airline_code": airline_code,
        "flight_code": flight_code,
        "flight_type": flight_type,
        "departure_city": departure_city,
        "arrival_city": arrival_city,
        "stop_type": num_stops,
        "flight_duration": duration_formatted,
        "departure_time": selected_times['departure_time'],
        "arrival_time": selected_times['arrival_time']
    }])
    
    if st.button("🚀 Predict"):
        try:
            
            preprocessor = joblib.load("artifacts/Pickle/preprocessor.pkl")
            model = joblib.load("artifacts/Pickle/model.pkl")

            prediction = model.predict(preprocessor.transform(prepared_data.basic_transformation(final_df)))[0]

            st.success(f"🎯 Predicted Flight Price: ₹{round(prediction):,}")
        
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
else:
    st.warning("No data available for this combination.")
