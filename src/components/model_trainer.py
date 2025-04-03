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
from src.utils import load_config
from src.exceptions import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_preparation import DataPreparation
from src.components.data_transformation import DataTransformation


warnings.filterwarnings("ignore", category=ConvergenceWarning)

class ModelTrainer:
    def __init__(self):
        config = load_config("config.yml")
        self.model_path = config['artifacts']['model_file']
        self.model_config = config['models']

        self.model_mapping = {
            # 'ElasticNet': ElasticNet,
            # 'LinearRegression': LinearRegression,
            # 'KNeighborsRegressor': KNeighborsRegressor,
            'DecisionTree': DecisionTreeRegressor,
            # 'RandomForest': RandomForestRegressor,
            # 'GradientBoosting': GradientBoostingRegressor,
            # 'AdaBoost': AdaBoostRegressor,
            # 'XGBoost': XGBRegressor,
        }

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            best_score = -float('inf')
            best_model_name = None
            best_model = None
            best_params = {}

            for model_name, hyperparams in self.model_config.items():
                if model_name not in self.model_mapping:
                    logging.warning(f"⚠️ Skipping unknown model '{model_name}' (not found in model_mapping)")
                    continue
    
                logging.info(f"Training model: {model_name}")
                model_class = self.model_mapping[model_name]
                model = model_class()

                param_grid = {f"{key}": val for key, val in hyperparams.items()}
                search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1, scoring='r2')
                search.fit(X_train, y_train)

                score = search.best_score_
                logging.info(f"{model_name} best CV score: {score}")
                logging.info(f"{model_name} best params: {search.best_params_}")

                if score > best_score:
                    best_score = score
                    best_model_name = model_name
                    best_model = search.best_estimator_
                    best_params = search.best_params_

            logging.info(f"Best model: {best_model_name} with score {best_score}")
            logging.info(f"Best hyperparameters: {best_params}")
            
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(best_model, self.model_path)
            logging.info(f"Saved best model to {self.model_path}")

        except Exception as e:
            raise CustomException(e, sys)

        
if __name__ == "__main__":
    
    data_ingestion = DataIngestion()
    train_set, test_set = data_ingestion.starting_ingestion()

    data_preparation = DataPreparation()
    train_data_transformed = data_preparation.basic_transformation(train_set, is_predict=False)
    test_data_transformed = data_preparation.basic_transformation(test_set, is_predict=False)

    transformer = DataTransformation()
    train_array, test_array = transformer.process_data(train_data_transformed, test_data_transformed)

    trainer = ModelTrainer()
    trainer.initiate_model_trainer(train_array, test_array)