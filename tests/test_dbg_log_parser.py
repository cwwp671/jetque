import unittest
from src.parsers.dbg_log_parser import DBGLogParser  # Relative import from the src package

class TestDBGLogParser(unittest.TestCase):

    def setUp(self):
        # Path to a sample dbg.txt file for testing
        self.dbg_file_path = "C:/Everquest/Logs/dbg.txt"
        self.parser = DBGLogParser(self.dbg_file_path)

    def test_parse_server_and_player(self):
        # Call the parser and get the results
        server_name, player_name, zone_name = self.parser.parse()

        # Assert that the expected results are returned
        self.assertIsNotNone(server_name)
        self.assertIsNotNone(player_name)
        self.assertIsNotNone(zone_name)

        # Optionally assert specific values
        self.assertEqual(server_name, "P1999Green")
        self.assertEqual(player_name, "Lifealerts")
        self.assertEqual(zone_name, "Kedge Keep")

if __name__ == "__main__":
    unittest.main()
