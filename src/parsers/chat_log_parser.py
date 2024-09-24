import re
from src.parsers.log_parser import LogParser
from src.events.event_handler import EventHandler


class ChatLogParser(LogParser):
    """
    A class for parsing chat log files and forwarding relevant events to the event handler.
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

    def __init__(self, log_file_path: str, event_handler: EventHandler) -> None:
        super().__init__(log_file_path)
        self.event_handler = event_handler  # Delegate event handling

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
        Identify if a log line contains a relevant event and forward it to the event handler.
        """
        if self.OUTGOING_COMBAT.search(line):
            self.event_handler.parse_event_line(line, 'outgoing_combat')
        elif self.OUTGOING_SKILL.search(line):
            self.event_handler.parse_event_line(line, 'outgoing_skill')
        elif self.OUTGOING_AVOIDANCE.search(line):
            self.event_handler.parse_event_line(line, 'outgoing_avoidance')
        elif self.INCOMING_COMBAT.search(line):
            self.event_handler.parse_event_line(line, 'incoming_combat')
        elif self.INCOMING_SKILL.search(line):
            self.event_handler.parse_event_line(line, 'incoming_skill')
        elif self.INCOMING_AVOIDANCE.search(line):
            self.event_handler.parse_event_line(line, 'incoming_avoidance')

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
