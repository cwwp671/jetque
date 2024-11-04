# jetque/src/parsers/chat_log_parser.py

import logging
from src.parsers.log_parser import LogParser
from src.events.event_factory import EventFactory
from src.events.event_manager import EventManager


class ChatLogParser(LogParser):
    """
    A class for parsing chat log files and forwarding relevant log lines to the event factory.
    """
    def __init__(self, log_file_path: str, event_handler: EventManager, event_factory: EventFactory) -> None:
        logging.debug("Here")
        super().__init__(log_file_path, default_interval=5)
        self.event_handler = event_handler
        self.event_factory = event_factory

    def set_timer_interval(self, default_interval: int) -> None:
        """Sets the timer interval from config, defaults to 5ms."""
        logging.debug("Here")
        interval = self.config.get("chat_log_timer", default_interval)
        self.timer.setInterval(interval)

    def process_log(self) -> None:
        """Processes new log lines and triggers events."""
        # logging.debug("Here - process_log called")
        if not self.is_running:
            logging.debug("Not running, returning")
            return

        new_lines = self.read_log()
        # logging.debug(f"New lines read: {len(new_lines)}")
        for line in new_lines:
            line = line.strip()
            # logging.debug(f"New line: {line}")
            self.parse_event_line(line)

    def parse_event_line(self, line: str) -> None:
        """
        Identify a log line and send it to the event factory, which creates the event.
        The created event is then sent to the event handler.
        """
        # logging.debug("Here")
        event = self.event_factory.create_event_from_line(line)  # Factory handles type determination

        if event:
            self.event_handler.add_event(event)
