import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils import load_all_configs
from src.logger import logging
from src.exceptions import CustomException


class DataIngestion:
    def __init__(self, test_size=0.2, random_state=42):
        self.config = load_all_configs()
        self.raw_path = self.config['artifacts']['raw_data_path']
        self.training_path = self.config['artifacts']['train_data_path']
        self.testing_path = self.config['artifacts']['test_data_path']
        self.test_size = test_size
        self.random_state = random_state

    def starting_ingestion(self):
        logging.info("🚀 Data Ingestion started.")
        try:
            if not os.path.exists(self.raw_path):
                raise FileNotFoundError(f"Raw data not found at: {self.raw_path}")

            raw_data = pd.read_csv(self.raw_path)
            logging.info(f"Raw data loaded from: {self.raw_path}")

            train_set, test_set = train_test_split(
                raw_data, test_size=self.test_size, random_state=self.random_state
            )

            train_set.to_csv(self.training_path, index=False)
            test_set.to_csv(self.testing_path, index=False)

            logging.info(f"Train data saved to {self.training_path} ({train_set.shape})")
            logging.info(f"Test data saved to {self.testing_path} ({test_set.shape})")
            logging.info("Data Ingestion completed successfully.")

            return train_set, test_set

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    loader = DataIngestion()
    loader.starting_ingestion()
