import json
import os

def load_config(config_file='jetque/config/config.json'):
    """
    Loads the configuration from a JSON file.

    :param config_file: Path to the configuration file.
    :return: A dictionary containing the configuration.
    """
    with open(config_file, 'r') as file:
        return json.load(file)
