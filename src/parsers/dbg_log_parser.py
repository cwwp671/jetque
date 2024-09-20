import re
import os

def parse_dbg_file(dbg_file_path):
    """
    Parses the dbg.txt file to extract the server name and player character name.

    :param dbg_file_path: Path to the dbg.txt file.
    :return: A tuple (server_name, player_name, zone_name) if found, otherwise (None, None, None).
    """
    server_name = None
    player_name = None
    zone_name = None

    if os.path.exists(dbg_file_path):
        with open(dbg_file_path, 'r') as dbg_file:
            lines = dbg_file.readlines()     #[-200:]  # Only check the last 200 lines for recent data

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

# Test function to run the parse_dbg_file() function
if __name__ == "__main__":
    dbg_file_path = "C:/Everquest/Logs/dbg.txt"  # Path to your dbg.txt file

    # Call the function and get the results
    server_name, player_name, zone_name = parse_dbg_file(dbg_file_path)

    # Print the results to verify correct parsing
    print(f"Server Name: {server_name}")
    print(f"Player Name: {player_name}")
    print(f"Zone Name: {zone_name}")
