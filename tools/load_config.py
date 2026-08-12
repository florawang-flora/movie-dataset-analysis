import yaml
from pathlib import Path 

def load_conf():
    current_file = Path(__file__)
    current_project_abs = current_file.parent.parent
    config_path = current_project_abs / 'config.yml'
    with open(config_path, 'r') as file: 
        return yaml.safe_load(file)