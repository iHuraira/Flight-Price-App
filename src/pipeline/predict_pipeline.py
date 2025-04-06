import os
import sys
import joblib
import pandas as pd
import numpy as np
import streamlit as st

from src.utils import load_object
from src.utils import load_all_configs
from src.exceptions import CustomException
from src.components.data_preparation import DataPreparation

class PredictPipeline:
    def __init__(self):
        self.config = load_all_configs()

    def predict(self, input_df: pd.DataFrame) -> float:
        try:
            model_path = os.path.join("artifacts","Pickle","model.pkl")

            preprocessor_path = os.path.join("artifacts","Pickle","preprocessor.pkl")

            model = joblib.load(model_path)
            preprocessor = joblib.load(preprocessor_path)

            prepared_data = DataPreparation().basic_transformation(input_df)
            
            prediction = model.predict(preprocessor.transform(prepared_data))[0]
            return prediction
        except Exception as e:
            raise CustomException(e, sys)
