# jetque/src/events/event_listener.py

import logging
from PyQt6.QtCore import QObject, pyqtSignal
from src.events.event_handler import EventHandler
from src.events.event_factory import EventFactory
from src.parsers.chat_log_parser import ChatLogParser
from src.events.event import CombatEvent, SkillEvent, AvoidanceEvent


class EventListener(QObject):
    # Define signals for future use
    combat_event_signal = pyqtSignal(str)
    skill_event_signal = pyqtSignal(str)
    avoidance_event_signal = pyqtSignal(str)

    def __init__(self, log_file_path: str):
        logging.debug("Here")
        super().__init__()
        self.event_handler = EventHandler()
        self.event_factory = EventFactory()
        self.parser = ChatLogParser(log_file_path, self.event_handler, self.event_factory)
        self.is_running = False  # New flag for stopping the loop

    def start_listening(self):
        """Start monitoring the log and processing events."""
        logging.debug("Here")
        self.is_running = True
        while self.is_running:
            self.parser.monitor_log()
            self.event_handler.process_event_queue()

    def stop_listening(self):
        """Gracefully stop the listening process."""
        self.is_running = False
