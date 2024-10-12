# jetque/src/parsers/dbg_log_parser.py

import re
import logging
from src.parsers.log_parser import LogParser

class DBGLogParser(LogParser):
    """
    Parses the EverQuest dbg.txt file to extract server, player, and zone information dynamically.
    Continuously monitors the file for real-time changes in game state.
    """

    def __init__(self, log_file_path: str) -> None:
        logging.debug("Here")
        super().__init__(log_file_path, default_interval=1000)
        self.server_name = None
        self.player_name = None
        self.zone_name = None

    def set_timer_interval(self, default_interval: int) -> None:
        """Sets the timer interval from config, defaults to 1000ms."""
        logging.debug("Here")
        interval = self.config.get("dbg_log_timer", default_interval)
        self.timer.setInterval(interval)

    def process_log(self) -> None:
        """Processes new lines for character, server, or zone information."""
        # logging.debug("Here - process_log called")
        if not self.is_running:
            logging.debug("Not running, returning")
            return

        new_lines = self.read_log()
        # logging.debug(f"New lines read: {len(new_lines)}")
        for line in new_lines:
            line = line.strip()
            logging.debug(f"New line: {line}")
            self.extract_info(line)

    def extract_info(self, line: str) -> None:
        """
        Parse an individual line to extract server, player, and zone information.
        """
        # logging.debug("Here")
        # Detect server
        server_match = re.search(r"WorldRPServer\s+message:\s+server\s+name\s+(\w+)", line)
        if server_match:
            self.server_name = server_match.group(1)
            logging.debug(f"Server Name Detected: {self.server_name}")

        # Detect player and zone
        player_match = re.search(r"Player\s*=\s*(\w+),\s*zone\s*=\s*([\w\s]+)", line)
        if player_match:
            self.player_name = player_match.group(1)
            self.zone_name = player_match.group(2).strip()  # Strip trailing spaces/newlines
            logging.debug(f"Player Name Detected: {self.player_name}, Zone Name Detected: {self.zone_name}")

        # Detect logout of a character (e.g., camping or quitting)
        if "*** EXITING: I have completed camping" in line or "*** DISCONNECTING: Quit command received" in line:
            self.player_name = None
            self.zone_name = None
            logging.debug("Player logged out, state reset.")
