import unittest
import os
from src.parsers.dbg_log_parser import DBGLogParser

class TestDBGLogParser(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary dbg log file for testing purposes.
        """
        self.log_file_path = 'test_dbg.txt'
        self.initial_content = (
            "2024-09-22 11:17:43 Starting EverQuest (Build Oct 31 2005 10:33:37)\n"
            "2024-09-22 11:18:52 WorldRPServer message: server name P1999Green\n"
            "2024-09-22 11:19:47 Player = Jetdru, zone = The Ruins of Old Paineel\n"
        )
        with open(self.log_file_path, 'w') as f:
            f.write(self.initial_content)
        self.parser = DBGLogParser(self.log_file_path)

    def tearDown(self):
        """
        Clean up the temporary log file after each test.
        """
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_read_full_log(self):
        """
        Test that the parser can correctly read and extract information from the dbg.txt.
        """
        server_name, player_name, zone_name = self.parser.read_full_log()
        self.assertEqual(server_name, "P1999Green")
        self.assertEqual(player_name, "Jetdru")
        self.assertEqual(zone_name, "The Ruins of Old Paineel")

    def test_server_switch(self):
        """
        Test the parser handles server switching correctly.
        """
        with open(self.log_file_path, 'a') as f:
            f.write("2024-09-22 11:20:00 WorldRPServer message: server name P1999Blue\n")
            f.write("2024-09-22 11:20:10 Player = AnotherChar, zone = Nektulos Forest\n")

        server_name, player_name, zone_name = self.parser.read_full_log()
        self.assertEqual(server_name, "P1999Blue")
        self.assertEqual(player_name, "AnotherChar")
        self.assertEqual(zone_name, "Nektulos Forest")

    def test_player_logout_and_relogin(self):
        """
        Test that the parser correctly resets on logout and captures new player information on relogin.
        """
        with open(self.log_file_path, 'a') as f:
            f.write("*** EXITING: I have completed camping\n")
            f.write("2024-09-22 11:21:00 Player = NewPlayer, zone = Qeynos\n")

        server_name, player_name, zone_name = self.parser.read_full_log()
        self.assertEqual(player_name, "NewPlayer")
        self.assertEqual(zone_name, "Qeynos")

    def test_multiple_logins(self):
        """
        Test that the parser handles multiple logins and logs out mid-session.
        """
        with open(self.log_file_path, 'a') as f:
            f.write("2024-09-22 11:22:00 Player = YetAnotherPlayer, zone = Misty Thicket\n")

        server_name, player_name, zone_name = self.parser.read_full_log()
        self.assertEqual(player_name, "YetAnotherPlayer")
        self.assertEqual(zone_name, "Misty Thicket")

if __name__ == '__main__':
    unittest.main()
