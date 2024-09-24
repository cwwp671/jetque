import re
from src.parsers.log_parser import LogParser
from src.events.event_factory import EventFactory
from src.events.event_handler import EventHandler


class ChatLogParser(LogParser):
    """
    A class for parsing chat log files and forwarding relevant log lines to the event factory.
    """

    COMBAT = (
        r'crush(?:es)?|punch(?:es)?|slash(?:es)?|pierce(?:s)?|hit(?:s)?|gore(?:s)?|'
        r'maul(?:s)?|bite(?:s)?|sting(?:s)?'
    )
    SKILL = r'backstab(?:s)?|kick(?:s)?|bash(?:es)?|strike(?:s)?'
    AVOIDANCE = r'dodge(?:s)?|block(?:s)?|parr(?:y|ies)|riposte(?:s)?|miss(?:es)?|magical skin absorbs the blow'

    OUTGOING_COMBAT = re.compile(rf'You ({COMBAT}) (\w+(\s\w+)?) for (\d+) points? of damage.')
    OUTGOING_SKILL = re.compile(rf'You ({SKILL}) (\w+(\s\w+)?) for (\d+) points? of damage.')
    OUTGOING_AVOIDANCE = re.compile(
        rf'You try to ({COMBAT}|{SKILL}) (\w+(\s\w+)?), but (\w+(\s\w+)?) ({AVOIDANCE})!'
    )

    INCOMING_COMBAT = re.compile(rf'(\w+(\s\w+)?) ({COMBAT}) YOU for (\d+) points? of damage.')
    INCOMING_SKILL = re.compile(rf'(\w+(\s\w+)?) ({SKILL}) YOU for (\d+) points? of damage.')
    INCOMING_AVOIDANCE = re.compile(
        rf'(\w+(\s\w+)?) tries to ({COMBAT}|{SKILL}) YOU, but YOU ({AVOIDANCE})!'
    )

    def __init__(self, log_file_path: str, event_handler: EventHandler, event_factory: EventFactory) -> None:
        super().__init__(log_file_path)
        self.event_handler = event_handler
        self.event_factory = event_factory

    def parse_log(self) -> None:
        """
        The required method from the parent LogParser class.
        This method processes the log to identify event lines.
        """
        self.reset_log_state()
        lines = self.read_log()
        for line in lines:
            self.parse_event_line(line)

    def parse_event_line(self, line: str) -> None:
        """
        Identify a log line and send it to the event factory, which creates the event.
        The created event is then sent to the event handler.
        """
        event = self.event_factory.create_event_from_line(line)  # Factory handles type determination

        if event:
            self.event_handler.add_event(event)

    def monitor_log(self) -> None:
        """
        Continuously monitor the chat log and forward relevant lines to the event handler.
        """
        while True:
            new_lines = self.read_log()
            if not new_lines:
                print("No new lines to process.")
            for line in new_lines:
                self.parse_event_line(line)
