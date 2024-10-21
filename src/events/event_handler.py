# jetque/src/events/event_handler.py

import logging
import pdb
import sys
from PyQt6.QtCore import QObject, pyqtSignal
from src.events.event import Event, CombatEvent, SkillEvent, AvoidanceEvent
from config.debug_config import is_debug_mode

class EventHandler(QObject):
    """
    Handles dispatching and processing of events from the queue to the appropriate areas.
    """

    incoming_event_signal = pyqtSignal(Event)
    outgoing_event_signal = pyqtSignal(Event)

    def __init__(self):
        super().__init__()
        # logging.debug("Initializing EventHandler")
        self.event_queue = []

    def add_event(self, event: Event) -> None:
        """
        Add an event to the event queue.
        """
        # logging.debug(f"Adding event to queue: {event}")
        self.event_queue.append(event)
        self.process_event_queue()

    def process_event_queue(self) -> None:
        """
        Process and dispatch events from the queue.
        """
        # logging.debug("Processing event queue")
        try:
            if self.event_queue:
                event = self.event_queue.pop(0)
                logging.debug(f"Dispatching event: {event}")
                self.dispatch_event(event)
        except Exception as e:
            logging.error(f"Error processing event queue: {e}")
            self.debug_breakpoint(condition=True)

    def dispatch_event(self, event: Event) -> None:
        """
        Dispatch event by emitting signals.
        """
        # logging.debug(f"Dispatching event: {event}")
        try:
            if event.event_category == 'incoming':
                self.incoming_event_signal.emit(event)
            elif event.event_category == 'outgoing':
                self.outgoing_event_signal.emit(event)
            else:
                logging.warning(f"Unhandled event category: {event.event_category}")
                self.debug_breakpoint(condition=True)
        except Exception as e:
            logging.error(f"Error dispatching event: {e}")
            self.debug_breakpoint(condition=True)

    def debug_breakpoint(self, condition=True):
        """
        Invoke pdb.set_trace() if the condition is True and in debug mode.
        """
        if is_debug_mode() and condition:
            logging.debug("Conditional breakpoint triggered in EventHandler")
            pdb.set_trace()

    @staticmethod
    def display_combat_event(event: CombatEvent) -> None:
        logging.debug(f"Displaying Combat Event: {event}")

    @staticmethod
    def display_skill_event(event: SkillEvent) -> None:
        logging.debug(f"Displaying Skill Event: {event}")

    @staticmethod
    def display_avoidance_event(event: AvoidanceEvent) -> None:
        logging.debug(f"Displaying Avoidance Event: {event} (Type: {event.avoidance_type})")
