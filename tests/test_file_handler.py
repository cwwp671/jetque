import unittest
import os
from src.utils.file_handler import FileHandler

class TestFileHandler(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary file for testing purposes.
        """
        self.test_file_path = 'test_file.txt'
        self.file_content = "Line 1\nLine 2\nLine 3\n"
        with open(self.test_file_path, 'w') as f:
            f.write(self.file_content)
        self.file_handler = FileHandler(self.test_file_path)

    def tearDown(self):
        """
        Clean up the temporary file after each test.
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_file_exists(self):
        """
        Test the file_exists method when the file exists and doesn't exist.
        """
        self.assertTrue(self.file_handler.file_exists())

        # Test when file does not exist
        os.remove(self.test_file_path)
        self.assertFalse(self.file_handler.file_exists())

    def test_read_lines(self):
        """
        Test that the read_lines method reads all lines correctly.
        """
        lines = self.file_handler.read_lines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "Line 1\n")
        self.assertEqual(lines[1], "Line 2\n")
        self.assertEqual(lines[2], "Line 3\n")

    def test_file_truncated(self):
        """
        Test the behavior when the file is truncated.
        """
        lines = self.file_handler.read_lines()
        self.assertEqual(len(lines), 3)

        # Simulate truncation
        with open(self.test_file_path, 'w') as f:
            f.write("New Line 1\n")

        # Read lines again after truncation
        lines = self.file_handler.read_lines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], "New Line 1\n")

    def test_read_lines_file_deleted(self):
        """
        Test the behavior when the file is deleted.
        """
        # Ensure lines are read first
        self.file_handler.read_lines()

        # Delete the file
        os.remove(self.test_file_path)

        # Try to read from the non-existing file
        lines = self.file_handler.read_lines()
        self.assertEqual(lines, [])
        self.assertEqual(self.file_handler.file_size, 0)

    def test_file_error_handling(self):
        """
        Test the handling of file-related errors.
        """
        # Simulate an unreadable file by opening it in write-only mode
        with open(self.test_file_path, 'w') as f:
            f.write("")

        # Attempt to read lines, expect empty due to error
        self.file_handler.file_path = "/invalid_path/nonexistent_file.txt"
        lines = self.file_handler.read_lines()
        self.assertEqual(lines, [])
        self.assertEqual(self.file_handler.file_size, 0)

if __name__ == '__main__':
    unittest.main()
