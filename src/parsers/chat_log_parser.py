import time
import os
from src.parsers.dbg_log_parser import parse_dbg_file

def find_chat_log_file(log_directory, dbg_file_path):
    """
    Determines the correct character's chat log file by parsing the dbg.txt file.

    :param log_directory: Path to the EverQuest logs directory.
    :param dbg_file_path: Path to the dbg.txt file.
    :return: Full path of the character's chat log file.
    """
    server_name, player_name, _ = parse_dbg_file(dbg_file_path)

    if server_name and player_name:
        chat_log_filename = f"eqlog_{player_name}_{server_name}.txt"
        chat_log_path = os.path.join(log_directory, chat_log_filename)

        if os.path.exists(chat_log_path):
            print(f"Found chat log for character: {player_name} on server: {server_name}")
            return chat_log_path
        else:
            print(f"Chat log file {chat_log_filename} not found in {log_directory}")
    else:
        print("Unable to determine active character and server from dbg.txt.")

    return None

def tail_log_file(log_file_path, check_interval=1):
    """
    Monitors the specified log file for new lines in real-time.

    :param log_file_path: Path to the chat log file.
    :param check_interval: How often to check for new lines (in seconds).
    """
    with open(log_file_path, 'r') as log_file:
        log_file.seek(0, os.SEEK_END)  # Start at the end of the file

        while True:
            line = log_file.readline()
            if not line:
                time.sleep(check_interval)  # Wait for new data
                continue
            process_log_line(line.strip())

def monitor_chat_log(log_file_path, check_interval=1):
    """
    Monitors the specified chat log file for new lines in real-time.

    :param log_file_path: Full path to the character's chat log file.
    :param check_interval: How often to check for new lines (in seconds).
    """
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            log_file.seek(0, os.SEEK_END)  # Start at the end of the file

            while True:
                line = log_file.readline()
                if not line:
                    time.sleep(check_interval)
                    continue
                process_log_line(line.strip())
    else:
        print(f"Chat log file not found: {log_file_path}")

def process_log_line(line):
    """
    Placeholder function to process each line from the log file.

    :param line: A new line from the chat log file.
    """
    print(f"New log line: {line}")
    # Add event parsing logic here
