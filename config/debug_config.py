# jetque/src/debug_config.py

import os

def is_debug_mode():
    """
    Determine if the application is running in debug mode.
    Controlled via the environment variable 'JETQUE_DEBUG'.
    """
    return os.getenv('JETQUE_DEBUG', 'True').lower() in ('true', '1', 't')
