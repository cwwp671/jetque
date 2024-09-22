import os

class LogParser:
    """
    Base class for handling log file operations with dynamic and stateless behavior.
    """
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.file_size = 0  # Track the size of the file to detect new data and handle truncation

    def file_exists(self):
        """
        Check if the log file exists and is accessible.
        """
        return os.path.exists(self.log_file_path)

    def read_lines(self):
        """
        Read new lines from the log file, handling dynamic user actions (truncation, renaming, deletion).
        """
        if not self.file_exists():
            # Handle file not existing gracefully, maybe log or retry later
            print(f"Log file '{self.log_file_path}' does not exist.")
            self.file_size = 0  # Reset the size since the file no longer exists
            return []

        current_size = os.path.getsize(self.log_file_path)

        # If the file was truncated or replaced, reset and read from the start
        if current_size < self.file_size:
            self.file_size = 0

        new_lines = []
        try:
            with open(self.log_file_path, 'r') as log_file:
                log_file.seek(self.file_size)  # Move to the last read position
                new_lines = log_file.readlines()  # Read new lines
                self.file_size = log_file.tell()  # Update file size for the next read
        except (FileNotFoundError, IOError):
            # Handle potential I/O errors gracefully (e.g., file deleted or inaccessible)
            print(f"Error reading the log file '{self.log_file_path}'. File might have been deleted or locked.")
            self.file_size = 0  # Reset the size to start over next time

        return new_lines
