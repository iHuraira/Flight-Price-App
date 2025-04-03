import yaml
from pathlib import Path
 
def load_yaml_file(file_path):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"⚠️ Config file not found: {file_path}")
    except yaml.YAMLError as e:
        print(f"⚠️ YAML format error in {file_path}: {e}")
    return {}
 
def load_all_configs(config_dir="config"):
    config_dir = Path(config_dir)
    
    config_files = [
        "artifacts.yml",
        "transformation.yml",
        "airports.yml",
        "features.yml",
        "model.yml",
    ]

    configs = {}
    for file in config_files:
        key = file.replace(".yml", "")
        configs[key] = load_yaml_file(config_dir / file)

    return configs