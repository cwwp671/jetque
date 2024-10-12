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
    logging.debug("Here 1")
    # Calculate the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logging.debug("Here 2")
    config_file_path = os.path.join(base_dir, config_file)
    logging.debug("Here 3")

    if not os.path.exists(config_file_path):
        logging.debug("Here 3.5")
        logging.debug(f"{config_file_path}")
        raise FileNotFoundError(f"Config file not found at {config_file_path}")

    logging.debug("Here 4")
    with open(config_file_path, 'r') as file:
        logging.debug("Here 4.5")
        return json.load(file)

def save_config(config_data, config_file='config/config.json'):
    """
    Saves the configuration to a JSON file.

    :param config_data: The dictionary containing the configuration to save.
    :param config_file: Path to the configuration file.
    """
    logging.debug("Here")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_file_path = os.path.join(base_dir, config_file)

    with open(config_file_path, 'w', encoding='utf-8') as file:
        json.dump(config_data, file, indent=4)
