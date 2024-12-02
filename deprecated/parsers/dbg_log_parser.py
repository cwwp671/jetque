# jetque/src/parsers/dbg_log_parser.py

import re
import logging
from PyQt6.QtCore import pyqtSignal
from src.parsers.log_parser import LogParser


class DBGLogParser(LogParser):
    """
    Parses the EverQuest dbg.txt file to extract server, player, and zone information dynamically.
    Continuously monitors the file for real-time changes in game state.
    """

    # Define new signals
    info_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, log_file_path: str) -> None:
        logging.debug("DBGLogParser: Initializing")
        super().__init__(log_file_path, default_interval=1000)
        self.server_name = None
        self.player_name = None
        self.zone_name = None

    def set_timer_interval(self, default_interval: int) -> None:
        """Sets the timer interval from config, defaults to 1000ms."""
        logging.debug("DBGLogParser: Setting timer interval")
        interval = self.config.get("dbg_log_timer", default_interval)
        self.timer.setInterval(interval)

    def process_log(self) -> None:
        """Processes new lines for character, server, or zone information."""
        logging.debug("DBGLogParser: Processing log")
        if not self.is_running:
            logging.debug("DBGLogParser: Not running, skipping processing")
            return

        new_lines = self.read_log()
        logging.debug(f"DBGLogParser: New lines read: {len(new_lines)}")
        for line in new_lines:
            line = line.strip()
            logging.debug(f"DBGLogParser: New line: {line}")
            try:
                self.extract_info(line)
            except Exception as e:
                logging.error(f"DBGLogParser: Error processing line '{line}': {e}")
                self.error_signal.emit(str(e))

    def extract_info(self, line: str) -> None:
        """
        Parse an individual line to extract server, player, and zone information.
        """
        # Detect server
        server_match = re.search(r"WorldRPServer\s+message:\s+server\s+name\s+(\w+)", line)
        if server_match:
            self.server_name = server_match.group(1)
            logging.debug(f"DBGLogParser: Server Name Detected: {self.server_name}")
            self.info_signal.emit(f"Server Name: {self.server_name}")

        # Detect player and zone
        player_match = re.search(r"Player\s*=\s*(\w+),\s*zone\s*=\s*([\w\s]+)", line)
        if player_match:
            self.player_name = player_match.group(1)
            self.zone_name = player_match.group(2).strip()  # Strip trailing spaces/newlines
            logging.debug(f"DBGLogParser: Player Name Detected: {self.player_name}, "
                          f"Zone Name Detected: {self.zone_name}")
            self.info_signal.emit(f"Player Name: {self.player_name}, Zone Name: {self.zone_name}")

        # Detect logout of a character (e.g., camping or quitting)
        if "*** EXITING: I have completed camping" in line or "*** DISCONNECTING: Quit command received" in line:
            self.player_name = None
            self.zone_name = None
            logging.debug("DBGLogParser: Player logged out, state reset.")
            self.info_signal.emit("Player logged out, state reset.")
