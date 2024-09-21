from src.parsers.dbg_log_parser import DBGLogParser
from src.parsers.chat_log_parser import ChatLogParser
from src.config_loader import load_config

# Load the configuration
config = load_config()

LOG_DIRECTORY = config.get('log_directory', "C:/Everquest/Logs")
DBG_FILE_PATH = os.path.join(LOG_DIRECTORY, config.get('dbg_file', "dbg.txt"))
CHECK_INTERVAL = config.get('check_interval', 1)

if __name__ == "__main__":
    # Initialize DBGLogParser
    dbg_parser = DBGLogParser(DBG_FILE_PATH)
    server_name, player_name, zone_name = dbg_parser.parse()

    if server_name and player_name:
        print(f"Found server: {server_name}, player: {player_name}, zone: {zone_name}")
        # Initialize ChatLogParser
        chat_log_file_path = f"{LOG_DIRECTORY}/eqlog_{player_name}_{server_name}.txt"
        chat_parser = ChatLogParser(chat_log_file_path)

        # Monitor the chat log for new events
        chat_parser.monitor()
    else:
        print("Failed to find server or player information.")
