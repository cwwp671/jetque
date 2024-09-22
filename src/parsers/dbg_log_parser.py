import re
from src.parsers.log_parser import LogParser

class DBGLogParser(LogParser):
    """
    A class for parsing the dbg.txt file to extract server, player, and zone information.
    This will only be invoked when a character login needs to be detected.
    """

    def __init__(self, log_file_path):
        super().__init__(log_file_path)
        self.server_name = None
        self.player_name = None
        self.zone_name = None

    def parse(self):
        """
        Parses the dbg.txt file to extract the server name, player name, and zone name.
        This is called only when character login needs to be detected.

        :return: A tuple (server_name, player_name, zone_name).
        """
        # Reset values before each parsing
        self.server_name = None
        self.player_name = None
        self.zone_name = None

        lines = self.read_lines()  # Inherited from LogParser

        for line in lines:
            # Match the server name
            server_match = re.search(r"WorldRPServer\s+message:\s+server\s+name\s+(\w+)", line)
            if server_match:
                self.server_name = server_match.group(1)

            # Match the player and zone info
            player_match = re.search(r"Player\s*=\s*(\w+),\s*zone\s*=\s*(\w+)", line)
            if player_match:
                self.player_name = player_match.group(1)
                self.zone_name = player_match.group(2)

        return self.server_name, self.player_name, self.zone_name
