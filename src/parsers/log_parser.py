from typing import List
from src.utils.file_handler import FileHandler

class LogParser:
    """
    A general-purpose log parser that focuses on log-specific tasks while delegating file operations.
    """
    def __init__(self, log_file_path: str) -> None:
        self.file_handler = FileHandler(log_file_path)
        self.current_log = []  # Store all lines read from the log file

    def read_log(self) -> List[str]:
        """
        Read new lines from the log file and update the current log.
        Check if the file exists before reading.
        """
        if not self.file_handler.file_exists():
            self.log_error(f"File {self.file_handler.file_path} does not exist.")
            return []

        new_lines = self.file_handler.read_lines()
        self.current_log.extend(new_lines)
        return new_lines

    def reset_log_state(self) -> None:
        """
        Reset the state of the log parser, clearing any stored data.
        Useful when switching characters or servers.
        """
        self.current_log = []

    def is_log_empty(self) -> bool:
        """
        Check if the log file is empty, indicating no data to process.
        """
        return len(self.current_log) == 0

    def get_full_log(self) -> List[str]:
        """
        Return the full log read so far.
        """
        return self.current_log

    def log_error(self, message: str) -> None:
        """
        Log any errors or events. Could be extended to write to a file or log system.
        """
        print(f"ERROR: {message}")

    def filter_log(self, pattern: str) -> List[str]:
        """
        Filter the current log based on a pattern (e.g., regex) and return the matching lines.
        """
        filtered_lines = [line for line in self.current_log if re.search(pattern, line)]
        return filtered_lines

    def parse_log(self):
        """
        Abstract method to be implemented by subclasses for specific log parsing.
        """
        raise NotImplementedError("This method should be implemented by a subclass")
