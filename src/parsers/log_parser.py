import os

class LogParser:
    """
    Base class for handling log file operations.
    """
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def file_exists(self):
        """
        Check if the log file exists.
        """
        return os.path.exists(self.log_file_path)

    def read_lines(self):
        """
        Read the entire log file.
        """
        if self.file_exists():
            with open(self.log_file_path, 'r') as log_file:
                return log_file.readlines()
        return []
