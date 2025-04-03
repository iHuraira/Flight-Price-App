import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils import load_config
from src.logger import logging
from src.exceptions import CustomException


class DataIngestion:
    def __init__(self):

        config = load_config("config.yml")
        
        self.raw_path = config['artifacts']['raw_data_path']
        self.training_path = config['artifacts']['train_data_path']
        self.testing_path = config['artifacts']['test_data_path']
        
    def starting_ingestion(self):
        logging.info("Data Ingestion has started")
        
        try:
            raw_data = pd.read_csv(self.raw_path)
            logging.info("Data has been loaded")
            
            train_set, test_set = train_test_split(raw_data, random_state=42, test_size=0.2)
            
            train_set.to_csv(self.training_path, index=False)
            logging.info(f"Training set saved with dimensions {train_set.shape}")
            
            test_set.to_csv(self.testing_path, index=False)
            logging.info(f"Testing set saved with dimensions {test_set.shape}")
            
            return train_set, test_set
        
        except CustomException as e:
            raise CustomException(e, sys)

