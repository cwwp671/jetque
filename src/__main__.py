import os
from src.parsers.chat_log_parser import find_chat_log_file, monitor_chat_log
from src.config_loader import load_config

# Load the configuration
config = load_config()

LOG_DIRECTORY = config.get('log_directory', "C:/Everquest/Logs")
DBG_FILE_PATH = os.path.join(LOG_DIRECTORY, config.get('dbg_file', "dbg.txt"))
CHECK_INTERVAL = config.get('check_interval', 1)

if __name__ == "__main__":
    # Find the correct chat log file using dbg.txt
    chat_log_file = find_chat_log_file(LOG_DIRECTORY, DBG_FILE_PATH)

    if chat_log_file:
        # Monitor the chat log for new events
        monitor_chat_log(chat_log_file, CHECK_INTERVAL)
    else:
        print("Failed to find the correct chat log file.")
