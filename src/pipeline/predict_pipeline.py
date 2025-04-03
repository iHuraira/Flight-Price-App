# src/pipeline/predict_pipeline.py

import joblib
import pandas as pd
from src.components.data_preparation import DataPreparation

class PredictPipeline:
    def __init__(self):
        try:
            self.preprocessor = joblib.load("artifacts/Pickle/preprocessor.pkl")
            self.model = joblib.load("artifacts/Pickle/model.pkl")
        except Exception as e:
            raise RuntimeError(f"Error loading model or preprocessor: {e}")

    def predict(self, input_df: pd.DataFrame) -> float:
        try:
            prepared_data = DataPreparation().basic_transformation(input_df)
            return self.model.predict(self.preprocessor.transform(prepared_data))[0]
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")
