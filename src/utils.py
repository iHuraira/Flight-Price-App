import os
import yaml
from pathlib import Path

def load_config(config_path="config.yml"):
    
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error loading YAML: {e}")
        return None

 
