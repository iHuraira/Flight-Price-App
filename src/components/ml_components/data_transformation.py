import os
import sys
import pickle
import numpy as np

from src.utils import load_config
from src.logger import logging
from src.exceptions import CustomException
from src.components.ml_components.data_ingestion import DataIngestion
from src.components.ml_components.data_preparation import DataPreparation

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder





class DataTransformation:
    def __init__(self):
        
        config = load_config("config.yml")
        
        self.save_path = config['artifacts']['preprocessor_path']

    def create_preprocessor(self):
        try:
            logging.info("Creating customized preprocessor with OneHot + Ordinal encoding")
            
            onehot_cols = [
                'airline_name', 'departure_city', 'flight_type',
                'arrival_city', 'arrival_time_of_day', 'departure_time_of_day'
            ]
            
            ordinal_cols = ['flight_code_category']
            
            onehot_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore'))
            ])

            ordinal_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OrdinalEncoder())
            ])
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('onehot', onehot_transformer, onehot_cols),
                    ('ordinal', ordinal_transformer, ordinal_cols)
                ],
                remainder='passthrough'
            )

            logging.info("Preprocessor successfully created")
            
            return preprocessor

        except Exception as e:
            logging.error("Error creating custom preprocessor")
            raise CustomException(e, sys)

    def process_data(self, train_df, test_df):
        try:
            logging.info("Creating preprocessing pipeline")
            preprocessing_object = self.create_preprocessor()

            target_column = "ticket_price"

            X_train = train_df.drop(columns=[target_column])
            y_train = train_df[target_column]

            X_test = test_df.drop(columns=[target_column])
            y_test = test_df[target_column]

            logging.info("Shapes before transformation:")
            logging.info(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
            logging.info(f"X_test: {X_test.shape}, y_test: {y_test.shape}")

            logging.info("Fitting and transforming training data")
            train_array = preprocessing_object.fit_transform(X_train)

            logging.info("Transforming test data")
            test_array = preprocessing_object.transform(X_test)

            logging.info("Shapes after transformation:")
            logging.info(f"train_array: {train_array.shape}")
            logging.info(f"test_array: {test_array.shape}")

            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            with open(self.save_path, 'wb') as f:
                pickle.dump(preprocessing_object, f)

            logging.info(f"Preprocessor saved to {self.save_path}")

            train_data = np.c_[train_array, y_train.to_numpy()]
            test_data = np.c_[test_array, y_test.to_numpy()]

            return train_data, test_data

        except Exception as e:
            logging.error("Error processing data with preprocessor")
            raise CustomException(e, sys)


