import unittest
import os
from src.parsers.log_parser import LogParser

class TestLogParser(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary log file for testing purposes.
        """
        self.log_file_path = 'test_log.txt'
        with open(self.log_file_path, 'w') as f:
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("Line 3\n")
        self.parser = LogParser(self.log_file_path)

    def tearDown(self):
        """
        Clean up the temporary log file after each test.
        """
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_file_exists(self):
        """
        Test that the log parser correctly detects the file existence.
        """
        self.assertTrue(self.parser.file_exists())

    def test_read_lines(self):
        """
        Test reading lines from a log file.
        """
        lines = self.parser.read_lines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "Line 1\n")
        self.assertEqual(lines[1], "Line 2\n")
        self.assertEqual(lines[2], "Line 3\n")

    def test_truncated_file(self):
        """
        Test if the parser correctly handles truncated files.
        """
        # Simulate truncating the file
        with open(self.log_file_path, 'w') as f:
            f.write("New Line 1\n")

        lines = self.parser.read_lines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], "New Line 1\n")

    def test_file_deletion(self):
        """
        Test that the parser handles file deletion gracefully.
        """
        os.remove(self.log_file_path)
        lines = self.parser.read_lines()
        self.assertEqual(lines, [])

if __name__ == '__main__':
    unittest.main()
