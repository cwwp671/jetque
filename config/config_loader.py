# jetque/config/config_loader.py

import json
import os
import logging

def load_config(config_file='jetque/config/config.json'):
    """
    Loads the configuration from a JSON file.

    :param config_file: Path to the configuration file.
    :return: A dictionary containing the configuration.
    """
    logging.debug("Loading configuration")
    # Calculate the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_file_path = os.path.join(base_dir, config_file)

    if not os.path.exists(config_file_path):
        logging.debug(f"{config_file_path}")
        raise FileNotFoundError(f"Config file not found at {config_file_path}")

    with open(config_file_path, 'r') as file:
        return json.load(file)

def save_config(config_data, config_file='jetque/config/config.json'):
    """
    Saves the configuration to a JSON file.

    :param config_data: The dictionary containing the configuration to save.
    :param config_file: Path to the configuration file.
    """
    logging.debug("Saving configuration")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_file_path = os.path.join(base_dir, config_file)

    with open(config_file_path, 'w', encoding='utf-8') as file:
        json.dump(config_data, file, indent=4)
