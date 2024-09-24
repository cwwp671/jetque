from src.events.event import Event, CombatEvent, SkillEvent, AvoidanceEvent


class EventHandler:
    """
    Handles dispatching and processing of events from the queue to the appropriate areas.
    """

    def __init__(self) -> None:
        self.event_queue = []

    def parse_event_line(self, line: str, event_type: str) -> None:
        """
        Process log line and create events based on type.
        """
        if event_type == 'outgoing_combat':
            # Parse and create a CombatEvent (example parsing shown, real parsing would be done with regex)
            self.create_event(CombatEvent, 'outgoing', 'combat', 'Player', 'Monster', 100)
        elif event_type == 'outgoing_skill':
            # Handle skill event creation here
            pass
        elif event_type == 'outgoing_avoidance':
            # Handle avoidance event creation here
            pass
        # Add other event types as necessary

    def create_event(self, event_class, event_category: str,
                     event_type: str, source: str, target: str, damage_value: int) -> None:
        """
        Create an event and add it to the queue.
        """
        event = event_class(event_category, event_type, source, target, damage_value)
        self.event_queue.append(event)
        print(f"Event created: {event}")

    def process_event_queue(self) -> None:
        """
        Process and dispatch events from the queue.
        """
        while self.event_queue:
            event = self.event_queue.pop(0)
            self.dispatch_event(event)

    def dispatch_event(self, event: Event) -> None:
        """
        Dispatch event to the correct visual area based on its type.
        """
        if isinstance(event, CombatEvent):
            self.display_combat_event(event)
        elif isinstance(event, SkillEvent):
            self.display_skill_event(event)
        elif isinstance(event, AvoidanceEvent):
            self.display_avoidance_event(event)

    @staticmethod
    def display_combat_event(event: CombatEvent) -> None:
        print(f"Displaying Combat Event: {event}")

    @staticmethod
    def display_skill_event(event: SkillEvent) -> None:
        print(f"Displaying Skill Event: {event}")

    @staticmethod
    def display_avoidance_event(event: AvoidanceEvent) -> None:
        print(f"Displaying Avoidance Event: {event}")
