# jetque/src/parsers/log_parser.py

import logging
from PyQt6.QtCore import QObject, QTimer
from typing import List
from src.utils.file_manager import FileManager
from config.config_loader import load_config

class LogParser(QObject):
    """
    A general-purpose log parser that focuses on log-specific tasks while delegating file operations.
    """
    def __init__(self, log_file_path: str, default_interval: int) -> None:
        logging.debug("Here")
        super().__init__()
        self.file_handler = FileManager(log_file_path)
        self.is_running = False
        self.config = load_config()
        self.timer = QTimer()
        self.set_timer_interval(default_interval)

    def set_timer_interval(self, default_interval: int) -> None:
        """Sets the interval of the timer based on the config or default."""
        logging.debug("Here")
        raise NotImplementedError("This method should be implemented by subclasses")

    def read_log(self) -> List[str]:
        """
        Read new lines from the log file using FileHandler.
        Only new lines should be processed.
        """
        # logging.debug("Here")
        return self.file_handler.read_lines()

    def monitor_log(self) -> None:
        """
        Continuously monitor the log file for changes and parse new lines.
        This is now the general monitor logic used across parsers unless a specific parser requires different behavior.
        """
        logging.debug("Here")
        self.is_running = True
        self.file_handler.initialize_position()
        logging.debug(f"monitoring at file position: {self.file_handler.file_size}")
        self.timer.timeout.connect(self.process_log)
        logging.debug("Timer connected to process_log")
        self.timer.start()
        logging.debug(f"Timer started with interval: {self.timer.interval()} ms")

    def process_log(self) -> None:
        """Processes new log lines."""
        logging.debug("Here")
        raise NotImplementedError("This method should be implemented by subclasses")

    def stop_monitoring(self) -> None:
        """Stop monitoring the log file."""
        logging.debug("Here")
        self.is_running = False
        self.timer.stop()
        logging.debug(f"Stopped monitoring at file position: {self.file_handler.file_size}")
