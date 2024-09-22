import re
import time
from src.parsers.log_parser import LogParser

class DBGLogParser(LogParser):
    """
    A class for parsing the dbg.txt file to extract server, player, and zone information.
    Handles dynamic EverQuest sessions and resets.
    """

    def __init__(self, log_file_path):
        super().__init__(log_file_path)
        self.server_name = None
        self.player_name = None
        self.zone_name = None

    def read_full_log(self):
        """
        Always read the dbg.txt from the start to ensure we don't miss any important data.
        """
        lines = self.read_lines()

        # Reset values before each parsing
        self.server_name = None
        self.player_name = None
        self.zone_name = None

        for line in lines:
            # Match the server name
            server_match = re.search(r"WorldRPServer\s+message:\s+server\s+name\s+(\w+)", line)
            if server_match:
                self.server_name = server_match.group(1)

            # Match the player and zone info
            player_match = re.search(r"Player\s*=\s*(\w+),\s*zone\s*=\s*([\w\s]+)", line)
            if player_match:
                self.player_name = player_match.group(1).strip()  # Strip any newlines or extra spaces
                self.zone_name = player_match.group(2).strip()  # Strip any newlines or extra spaces

        return self.server_name, self.player_name, self.zone_name

    def monitor(self):
        """
        Monitors the dbg.txt file for events in real-time (character login, logout, server switch).
        Continuously reads the file to track live updates.
        """
        last_seen_player = None
        while True:
            new_lines = self.read_lines()
            if new_lines:
                for line in new_lines:
                    self.parse_line(line, last_seen_player)
            time.sleep(1)  # Monitor the file continuously for new updates

    def parse_line(self, line, last_seen_player):
        """
        Parse individual lines and manage session activity, including switching characters.
        """
        # Detect a new EverQuest session (start of a new session)
        if "Starting EverQuest" in line:
            print("New EverQuest session detected.")
            self.server_name = None
            self.player_name = None
            self.zone_name = None

        # Detect logout of a character (e.g., camping or quitting)
        if "*** EXITING: I have completed camping" in line or "*** DISCONNECTING: Quit command received" in line:
            print("Player logged out, resetting character state.")
            self.player_name = None
            self.zone_name = None

        # Detect the current player and server
        server_match = re.search(r"WorldRPServer\s+message:\s+server\s+name\s+(\w+)", line)
        if server_match:
            self.server_name = server_match.group(1)

        player_match = re.search(r"Player\s*=\s*(\w+),\s*zone\s*=\s*([\w\s]+)", line)
        if player_match:
            self.player_name = player_match.group(1).strip()  # Strip any newlines or extra spaces
            self.zone_name = player_match.group(2).strip()  # Strip any newlines or extra spaces

        # Handle character switching
        if self.player_name != last_seen_player:
            print(f"Switching to character {self.player_name} on server {self.server_name}")
            last_seen_player = self.player_name
