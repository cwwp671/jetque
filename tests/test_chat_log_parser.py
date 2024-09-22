import unittest
import os
from src.parsers.chat_log_parser import ChatLogParser, CombatEvent

class TestChatLogParser(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary chat log file for testing purposes.
        """
        self.log_file_path = 'test_chat_log.txt'
        self.parser = ChatLogParser(self.log_file_path)
        self.initial_content = (
            "You crush a goblin for 55 points of damage.\n"
            "A goblin slashes YOU for 30 points of damage.\n"
        )
        with open(self.log_file_path, 'w') as f:
            f.write(self.initial_content)

    def tearDown(self):
        """
        Clean up the temporary chat log file after each test.
        """
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_parse_outgoing_combat_event(self):
        """
        Test that the parser can correctly generate an outgoing combat event.
        """
        self.parser.parse_log()
        self.assertEqual(len(self.parser.events), 2)
        event = self.parser.events[0]
        self.assertIsInstance(event, CombatEvent)
        self.assertEqual(event.event_type, 'outgoing')
        self.assertEqual(event.damage_type, 'crush')
        self.assertEqual(event.source, 'Player')
        self.assertEqual(event.target, 'a goblin')
        self.assertEqual(event.damage_value, 55)

    def test_parse_incoming_combat_event(self):
        """
        Test that the parser can correctly generate an incoming combat event.
        """
        self.parser.parse_log()
        self.assertEqual(len(self.parser.events), 2)
        event = self.parser.events[1]
        self.assertIsInstance(event, CombatEvent)
        self.assertEqual(event.event_type, 'incoming')
        self.assertEqual(event.damage_type, 'slashes')
        self.assertEqual(event.source.lower(), 'a goblin')  # Compare lowercase to ignore case sensitivity
        self.assertEqual(event.target, 'Player')
        self.assertEqual(event.damage_value, 30)

    def test_safe_int_conversion(self):
        """
        Test that the parser can safely convert strings to integers and handle invalid data.
        """
        valid_value = self.parser.safe_int("123")
        invalid_value = self.parser.safe_int("invalid")

        self.assertEqual(valid_value, 123)
        self.assertEqual(invalid_value, 0)

    def test_no_combat_events(self):
        """
        Test that the parser handles an empty or unrelated log file without errors.
        """
        with open(self.log_file_path, 'w') as f:
            f.write("This is not a combat log entry.\n")

        self.parser.parse_log()
        self.assertEqual(len(self.parser.events), 0)

    def test_multiple_combat_events(self):
        """
        Test that the parser handles multiple combat events in sequence.
        """
        additional_content = (
            "You punch a bat for 40 points of damage.\n"
            "A bat bites YOU for 25 points of damage.\n"
        )
        with open(self.log_file_path, 'a') as f:
            f.write(additional_content)

        self.parser.parse_log()
        self.assertEqual(len(self.parser.events), 4)
        first_event = self.parser.events[2]
        self.assertEqual(first_event.event_type, 'outgoing')
        self.assertEqual(first_event.damage_type, 'punch')
        self.assertEqual(first_event.source, 'Player')
        self.assertEqual(first_event.target, 'a bat')
        self.assertEqual(first_event.damage_value, 40)

if __name__ == '__main__':
    unittest.main()
