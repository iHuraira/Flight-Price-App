import pandas as pd

class FlightInputModel:
    def __init__(self, airline_name, airline_code, flight_code, flight_type,
                 departure_city, arrival_city, stop_type, flight_duration,
                 departure_time, arrival_time):
        self.data = {
            "airline_name": airline_name,
            "airline_code": airline_code,
            "flight_code": flight_code,
            "flight_type": flight_type,
            "departure_city": departure_city,
            "arrival_city": arrival_city,
            "stop_type": stop_type,
            "flight_duration": flight_duration,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
        }

    def to_dataframe(self):
        return pd.DataFrame([self.data])
