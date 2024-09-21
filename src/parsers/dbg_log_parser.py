import re
from src.parsers.log_parser import LogParser

class DBGLogParser(LogParser):
    """
    A class for parsing the dbg.txt file to extract server, player, and zone information.
    """
    def parse(self):
        """
        Parses the dbg.txt file to extract the server name, player name, and zone name.

        :return: A tuple (server_name, player_name, zone_name).
        """
        server_name = None
        player_name = None
        zone_name = None

        lines = self.read_lines()  # Inherited from LogParser

        for line in lines:
            # Match the server name
            server_match = re.search(r"WorldRPServer\s+message:\s+server\s+name\s+(\w+)", line)
            if server_match:
                server_name = server_match.group(1)

            # Match the player and zone info
            player_match = re.search(r"Player\s*=\s*(\w+),\s*zone\s*=\s*(\w+)", line)
            if player_match:
                player_name = player_match.group(1)
                zone_name = player_match.group(2)

        return server_name, player_name, zone_name
