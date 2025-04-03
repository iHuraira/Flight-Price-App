import os
import sys
import pickle
import pandas as pd

from src.utils import load_config
from src.logger import logging
from src.exceptions import CustomException

class DataPreparation:
    def __init__(self):
        config = load_config("config.yml")
    
        self.renaming_dictionary = config['datatransformation']['COLUMN_RENAME_MAPPING']
        self.stop_area = config.get('stop_area_dict', {})
        self.selected_columns = config.get('selected_columns', [])
        self.threshold_path = config['artifacts']['threshold_path']
        self.target_column = 'ticket_price'

        logging.info("Data transformation has been started")

    def save_flight_code_stats(self, df, artifacts_path):
        flight_code_counts = df['flight_code'].value_counts()
        high_threshold = float(flight_code_counts.quantile(0.75))
        low_threshold = float(flight_code_counts.quantile(0.25))
    
        stats = {
            'counts': flight_code_counts.to_dict(),
            'high': high_threshold,
            'low': low_threshold
        }
    
        os.makedirs(os.path.dirname(artifacts_path), exist_ok=True)
        with open(artifacts_path, 'wb') as f:
            pickle.dump(stats, f)
    
        return stats['counts'], stats['high'], stats['low']

    def load_flight_code_stats(self, artifacts_path):
        with open(artifacts_path, 'rb') as f:
            stats = pickle.load(f)
        return stats['counts'], stats['high'], stats['low']

    def process_flight_data(self, df):
        df['departure_time'] = pd.to_datetime(df['departure_time'], format='%H:%M')
        df['arrival_time'] = pd.to_datetime(df['arrival_time'], format='%H:%M')

        def time_of_day(hour):
            if 6 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 18:
                return 'Afternoon'
            elif 18 <= hour < 21:
                return 'Evening'
            else:
                return 'Night'

        df['departure_time_of_day'] = df['departure_time'].dt.hour.apply(time_of_day)
        df['arrival_time_of_day'] = df['arrival_time'].dt.hour.apply(time_of_day)

        def duration_in_minutes(duration):
            hours, minutes = 0, 0
            try:
                if 'h' in duration:
                    hours = int(duration.split('h')[0].strip())
                if 'm' in duration:
                    minutes = int(duration.split('h')[1].split('m')[0].strip())
                elif '.' in duration:
                    hours, minutes = map(int, duration.split('.'))
            except ValueError:
                hours, minutes = 0, 0
            return hours * 60 + minutes

        df['flight_duration_minutes'] = df['flight_duration'].apply(duration_in_minutes)

        df['delay_duration_minutes'] = (df['arrival_time'] - df['departure_time']).dt.total_seconds() / 60
        df['is_late'] = (df['delay_duration_minutes'] > 0).astype(int)
        df['is_overnight'] = (df['arrival_time'] < df['departure_time']).astype(int)
        df['is_early'] = (df['delay_duration_minutes'] < 0).astype(int)

        df.drop(columns=['departure_time', 'arrival_time', 'flight_duration'], inplace=True)
        return df

    def add_stop_columns(self, data):
        data['num_stops'] = data['stop_type'].apply(lambda x: 0 if 'non-stop' in x else (1 if '1-stop' in x else 2))
        data['stop_area'] = data['stop_type'].apply(lambda x: "None" if 'non-stop' in x else 
                                                    (x.split("Via")[-1].strip() if 'Via' in x else "None"))
        
        data['stop_area'] = data['stop_area'].map(self.stop_area).fillna('not defined')
        data.loc[data['num_stops'] == 0, 'stop_area'] = "None"
        data.drop('stop_type', axis=1, inplace=True)
        return data

    def create_flight_code_features_dynamic(self, df, flight_code_counts, high_threshold, low_threshold):
        df['flight_code_count'] = df['flight_code'].map(flight_code_counts).fillna(0)
        df['is_frequent_route'] = df['flight_code_count'] > high_threshold

        def categorize_by_dynamic_frequency(count):
            if count >= high_threshold:
                return 'High'
            elif count >= low_threshold:
                return 'Medium'
            else:
                return 'Low'

        df['flight_code_category'] = df['flight_code_count'].apply(categorize_by_dynamic_frequency)
        df['is_rare_flight'] = df['flight_code_count'].apply(lambda x: 1 if x == 1 else 0)

        df.drop(columns=['flight_code', 'flight_code_count'], inplace=True)
        return df

    def basic_transformation(self, data, is_predict=True):
        logging.info("Basic transformation in progress")
        data.rename(columns=self.renaming_dictionary, inplace=True)
        logging.info("Columns renamed based on configuration")

        try:
            if is_predict:
                logging.info("Loading precomputed flight code statistics for prediction")
                flight_code_counts, high_threshold, low_threshold = self.load_flight_code_stats(self.threshold_path)
            else:
                logging.info("Computing and saving flight code statistics for training")
                flight_code_counts, high_threshold, low_threshold = self.save_flight_code_stats(data, self.threshold_path)

            logging.info("Starting flight data processing")
            data = self.process_flight_data(data)
            logging.info("Flight timing and duration features created")

            logging.info("Creating stop-related features")
            data = self.add_stop_columns(data)
            logging.info("Stop-related features added")

            logging.info("Applying flight code frequency-based features")
            data = self.create_flight_code_features_dynamic(data, flight_code_counts, high_threshold, low_threshold)
            logging.info("Flight code features added successfully")

            logging.info("Mapping 'is_frequent_route' to binary format")
            data['is_frequent_route'] = data['is_frequent_route'].map({True: 0, False: 1})

            logging.info("Dropping unnecessary columns: ['flight_date', 'airline_code', 'stop_area']")
            data.drop(columns=['flight_date', 'airline_code', 'stop_area'], inplace=True, errors='ignore')

            if not is_predict:
                logging.info("Cleaning and converting target column 'ticket_price'")
                data[self.target_column] = data[self.target_column].replace({r'[^\d.]': ''}, regex=True).astype(int)
            else:
                if self.target_column in data.columns:
                    logging.info("Dropping target column 'ticket_price' during prediction")
                    data.drop(columns=[self.target_column], inplace=True)

            logging.info("Basic transformation completed successfully")
            return data

        except CustomException as e:
            logging.error("Error occurred during basic transformation")
            raise CustomException(e, sys)
        
        
if __name__ == "__main__":
    
    example_data = pd.DataFrame([{
        'date': '11-02-2022',
        'airline': 'Air India',
        'ch_code': 'AI',
        'num_code': 868,
        'dep_time': '18:00',
        'from': 'Delhi',
        'time_taken': '02h 00m',
        'stop': 'non-stop ',
        'arr_time': '20:00',
        'to': 'Mumbai',
        'flight_type': 'business'
    }])

    data_preparation = DataPreparation()
    
    prepared_data = data_preparation.basic_transformation(example_data, is_predict=True)
    
    print(prepared_data[['airline_name', 'departure_city', 'arrival_city', 'flight_type',
       'departure_time_of_day', 'arrival_time_of_day']])
    print(prepared_data.columns)

    # transformer = DataTransformation()
    # train_array, test_array = transformer.process_data(train_data_transformed, test_data_transformed)

    # trainer = ModelTrainer()
    # trainer.initiate_model_trainer(train_array, test_array)
        
