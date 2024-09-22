import os
from typing import List

class FileHandler:
    """
    Handles the low-level file interactions such as reading lines, checking existence, and monitoring file size.
    """
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.file_size = 0

    def file_exists(self) -> bool:
        """
        Check if the file exists.
        """
        return os.path.exists(self.file_path)

    def read_lines(self) -> List[str]:
        """
        Read new lines from the file, handling truncation and I/O errors gracefully.
        """
        if not self.file_exists():
            print(f"File '{self.file_path}' does not exist.")
            self.file_size = 0
            return []

        current_size = os.path.getsize(self.file_path)
        if current_size < self.file_size:
            # File has been truncated
            self.file_size = 0

        new_lines = []
        try:
            with open(self.file_path, 'r') as file:
                file.seek(self.file_size)
                new_lines = file.readlines()
                self.file_size = file.tell()
        except (FileNotFoundError, IOError):
            print(f"Error reading the file '{self.file_path}'.")
            self.file_size = 0

        return new_lines
