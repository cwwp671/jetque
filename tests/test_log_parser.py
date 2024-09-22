import unittest
import os
from unittest.mock import MagicMock
from src.parsers.log_parser import LogParser
from src.utils.file_handler import FileHandler

class TestLogParser(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary log file for testing purposes and mock the file handler.
        """
        self.log_file_path = 'test_log.txt'
        with open(self.log_file_path, 'w') as f:
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("Line 3\n")
        self.parser = LogParser(self.log_file_path)

        # Mock the FileHandler for cases like file deletion
        self.parser.file_handler = MagicMock(spec=FileHandler)
        self.parser.file_handler.file_path = self.log_file_path
        self.parser.file_handler.read_lines = MagicMock(return_value=["Line 1\n", "Line 2\n", "Line 3\n"])
        self.parser.file_handler.file_exists = MagicMock(return_value=True)

    def tearDown(self):
        """
        Clean up the temporary log file after each test.
        """
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_file_exists(self):
        """
        Test that the log parser correctly detects the file existence through the FileHandler.
        """
        self.assertTrue(self.parser.file_handler.file_exists())
        self.parser.file_handler.file_exists.assert_called_once()

    def test_read_lines(self):
        """
        Test reading lines from a log file using the FileHandler.
        """
        lines = self.parser.read_log()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "Line 1\n")
        self.assertEqual(lines[1], "Line 2\n")
        self.assertEqual(lines[2], "Line 3\n")
        self.parser.file_handler.read_lines.assert_called_once()

    def test_truncated_file(self):
        """
        Test if the parser correctly handles truncated files.
        """
        # Simulate truncating the file
        self.parser.file_handler.read_lines = MagicMock(return_value=["New Line 1\n"])

        lines = self.parser.read_log()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], "New Line 1\n")
        self.parser.file_handler.read_lines.assert_called_once()

    def test_file_deletion(self):
        """
        Test that the parser handles file deletion gracefully.
        """
        # Mock the file_exists method to simulate file deletion
        self.parser.file_handler.file_exists = MagicMock(return_value=False)

        # Mock the read_lines method
        self.parser.file_handler.read_lines = MagicMock(return_value=[])

        # Call the method to read the log after file deletion
        lines = self.parser.read_log()

        # Check that the parser handles the deletion by returning no lines
        self.assertEqual(lines, [])

        # Assert that file_exists was called once
        self.parser.file_handler.file_exists.assert_called_once()

        # Assert that read_lines was not called since the file doesn't exist
        self.parser.file_handler.read_lines.assert_not_called()

    def test_reset_log_state(self):
        """
        Test resetting the log state.
        """
        # Read the log to populate the current_log
        self.parser.read_log()
        self.assertEqual(len(self.parser.get_full_log()), 3)

        # Reset the log state and confirm it's cleared
        self.parser.reset_log_state()
        self.assertEqual(len(self.parser.get_full_log()), 0)

if __name__ == '__main__':
    unittest.main()
