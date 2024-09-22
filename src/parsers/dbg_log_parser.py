import re
import time
from src.parsers.log_parser import LogParser

class DBGLogParser(LogParser):
    """
    Parses the EverQuest dbg.txt file to extract server, player, and zone information dynamically.
    Continuously monitors the file for real-time changes in game state.
    """

    def __init__(self, log_file_path: str) -> None:
        super().__init__(log_file_path)
        self.server_name = None
        self.player_name = None
        self.zone_name = None

    def parse_log(self) -> None:
        """
        The required method from the parent LogParser class.
        This method processes the log to extract relevant information about the game session.
        """
        self.reset_log_state()  # Clear previous log data
        lines = self.read_log()  # Read the entire log
        for line in lines:
            self.extract_info(line)  # Extract relevant info from each line

    def extract_info(self, line: str) -> None:
        """
        Parse an individual line to extract server, player, and zone information.
        """
        # Detect server
        server_match = re.search(r"WorldRPServer\s+message:\s+server\s+name\s+(\w+)", line)
        if server_match:
            self.server_name = server_match.group(1)

        # Detect player and zone
        player_match = re.search(r"Player\s*=\s*(\w+),\s*zone\s*=\s*([\w\s]+)", line)
        if player_match:
            self.player_name = player_match.group(1)
            self.zone_name = player_match.group(2).strip()  # Strip trailing spaces/newlines

        # Detect logout of a character (e.g., camping or quitting)
        if "*** EXITING: I have completed camping" in line or "*** DISCONNECTING: Quit command received" in line:
            print("Player logged out, resetting character state.")
            self.player_name = None
            self.zone_name = None

    def monitor_log(self) -> None:
        """
        Continuously monitor the dbg.txt file for real-time events (character login, logout, server switch).
        """
        while True:
            new_lines = self.read_log()
            for line in new_lines:
                self.extract_info(line)
            time.sleep(1)  # Poll every second
