import unittest
from unittest.mock import MagicMock
from src.parsers.chat_log_parser import ChatLogParser
from src.events.event_factory import EventFactory
from src.events.event_handler import EventHandler


class TestChatLogParser(unittest.TestCase):

    def setUp(self):
        self.event_factory = MagicMock(EventFactory)
        self.event_handler = MagicMock(EventHandler)
        self.chat_log_parser = ChatLogParser("fake_log_path", self.event_handler, self.event_factory)

    def simulate_log_parsing(self, log_lines):
        """
        Helper method to simulate reading the log lines and parsing them.
        """
        self.chat_log_parser.read_log = MagicMock(return_value=log_lines)
        self.chat_log_parser.parse_log()

    def assert_event_factory_called_with(self, log_line):
        """
        Helper method to check if the event factory was called with the correct log line.
        """
        self.event_factory.create_event_from_line.assert_called_once_with(log_line)

    def test_event_parsing(self):
        cases = [
            {'log_line': "You crush a goblin for 50 points of damage.", 'description': 'Outgoing Combat'},
            {'log_line': "You backstab a rat for 60 points of damage.", 'description': 'Outgoing Skill'},
            {'log_line': "You try to crush a goblin, but the goblin dodges!", 'description': 'Outgoing Avoidance'},
            {'log_line': "A goblin crushes YOU for 30 points of damage.", 'description': 'Incoming Combat'},
            {'log_line': "A goblin backstabs YOU for 40 points of damage.", 'description': 'Incoming Skill'},
            {'log_line': "A goblin tries to crush YOU, but YOU dodge!", 'description': 'Incoming Avoidance'},
            {'log_line': "You say, 'Hello!'", 'description': 'Irrelevant'}
        ]

        for case in cases:
            with self.subTest(case=case):
                log_lines = [case['log_line']]

                # Set up the mock to return None or a mock event, depending on the case
                if case['description'] == 'Irrelevant':
                    self.event_factory.create_event_from_line.return_value = None
                else:
                    self.event_factory.create_event_from_line.return_value = MagicMock()

                self.simulate_log_parsing(log_lines)

                # Check if the event factory was called with the correct log line
                self.assert_event_factory_called_with(case['log_line'])

                if case['description'] == 'Irrelevant':
                    # Ensure no event was added to the handler for irrelevant lines
                    self.event_handler.add_event.assert_not_called()
                else:
                    # Ensure the event was added to the handler for relevant lines
                    self.event_handler.add_event.assert_called_once()

                # Reset mocks between tests
                self.event_factory.reset_mock()
                self.event_handler.reset_mock()


if __name__ == '__main__':
    unittest.main()
