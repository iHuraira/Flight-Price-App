import os
import sys
import joblib
import warnings

from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.exceptions import ConvergenceWarning
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import ElasticNet, LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor
)

from src.logger import logging
from src.utils import load_all_configs
from src.exceptions import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_preparation import DataPreparation
from src.components.data_transformation import DataTransformation

warnings.filterwarnings("ignore", category=ConvergenceWarning)

class ModelTrainer:
    def __init__(self):
        self.config = load_all_configs()
        self.model_path = self.config["artifacts"]["model_file"]

        self.model_config = self.config["model"]["model_selection"]["models"]
        self.active_model = self.config["model"]["model_selection"]["active_model"]

        self.model_mapping = {
            "ElasticNet": ElasticNet,
            "LinearRegression": LinearRegression,
            "KNeighborsRegressor": KNeighborsRegressor,
            "DecisionTree": DecisionTreeRegressor,
            "RandomForest": RandomForestRegressor,
            "GradientBoosting": GradientBoostingRegressor,
            "AdaBoost": AdaBoostRegressor,
            "XGBoost": XGBRegressor,
        }

        if self.active_model not in self.model_mapping:
            raise ValueError(f"Active model '{self.active_model}' not found in model_mapping.")


    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            model_class = self.model_mapping[self.active_model]
            model = model_class()

            param_grid = self.model_config[self.active_model]

            logging.info(f"Training model: {self.active_model}")
            search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1, scoring='r2')
            search.fit(X_train, y_train)

            best_model = search.best_estimator_
            best_score = search.best_score_
            best_params = search.best_params_

            logging.info(f"Best model: {self.active_model} with score {best_score}")
            logging.info(f"Best hyperparameters: {best_params}")

            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(best_model, self.model_path)
            logging.info(f"Saved best model to {self.model_path}")

        except Exception as e:
            raise CustomException(e, sys)
