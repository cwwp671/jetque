# jetque/src/events/event_handler.py

import logging
from src.events.event import Event, CombatEvent, SkillEvent, AvoidanceEvent

class EventHandler:
    """
    Handles dispatching and processing of events from the queue to the appropriate areas.
    """

    def __init__(self) -> None:
        logging.debug("Initializing EventHandler")
        self.event_queue = []

    def add_event(self, event: Event) -> None:
        """
        Add an event to the event queue.
        """
        logging.debug(f"Adding event to queue: {event}")
        self.event_queue.append(event)

    def process_event_queue(self) -> None:
        """
        Process and dispatch events from the queue.
        """
        logging.debug("Processing event queue")
        while self.event_queue:
            event = self.event_queue.pop(0)
            logging.debug(f"Dispatching event: {event}")
            self.dispatch_event(event)

    def dispatch_event(self, event: Event) -> None:
        """
        Dispatch event to the correct visual area based on its type.
        """
        logging.debug(f"Dispatching event based on type: {event.event_type}")
        if isinstance(event, CombatEvent):
            self.display_combat_event(event)
        elif isinstance(event, SkillEvent):
            self.display_skill_event(event)
        elif isinstance(event, AvoidanceEvent):
            self.display_avoidance_event(event)
        else:
            logging.warning(f"Unhandled event type: {event.event_type}")

    @staticmethod
    def display_combat_event(event: CombatEvent) -> None:
        logging.debug(f"Displaying Combat Event: {event}")

    @staticmethod
    def display_skill_event(event: SkillEvent) -> None:
        logging.debug(f"Displaying Skill Event: {event}")

    @staticmethod
    def display_avoidance_event(event: AvoidanceEvent) -> None:
        logging.debug(f"Displaying Avoidance Event: {event} (Type: {event.avoidance_type}")
