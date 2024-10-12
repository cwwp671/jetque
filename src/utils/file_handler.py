# jetque/src/utils/file_handler.py

import os
import logging
from typing import List

class FileHandler:
    """
    Handles the low-level file interactions such as reading lines, checking existence, and monitoring file size.
    """
    def __init__(self, file_path: str) -> None:
        logging.debug("Here")
        self.file_path = file_path
        self.file_size = 0

    def file_exists(self) -> bool:
        """
        Check if the file exists.
        """
        # logging.debug("Here")
        return os.path.exists(self.file_path)

    def initialize_position(self) -> None:
        """
        Initialize the file position either at the last known position or at the end of the file.
        This ensures the parser doesn't read old lines on start or restart.
        """
        logging.debug("Here")
        if self.file_exists():
            with open(self.file_path, 'r') as file:
                file.seek(0, 2)  # Move to the end of the file if starting fresh
                self.file_size = file.tell()  # Update file size to end of file
                logging.debug(f"Initialized file position to: {self.file_size}")

    def read_lines(self) -> List[str]:
        """
        Read new lines from the file, starting from the last known position.
        This prevents reprocessing old lines and only processes newly appended ones.
        """
        # logging.debug("Here")
        if not self.file_exists():
            logging.debug(f"File '{self.file_path}' does not exist.")
            self.file_size = 0
            return []

        current_size = os.path.getsize(self.file_path)

        # If the file was truncated, jump to the current end of the file instead of resetting to 0
        if current_size < self.file_size:
            logging.debug(f"File '{self.file_path}' was truncated. Adjusting to the current end of the file.")
            self.file_size = current_size
            return []

        new_lines = []
        try:
            with open(self.file_path, 'r') as file:
                file.seek(self.file_size)  # Start reading from the last known position
                new_lines = file.readlines()  # Read any new lines added to the file
                self.file_size = file.tell()  # Update the file size after reading new lines
                # logging.debug(f"Updated file position to: {self.file_size}")
        except (FileNotFoundError, IOError):
            logging.debug(f"Error reading the file '{self.file_path}'.")
            self.file_size = 0

        return new_lines
