# jetque/src/events/event.py

import logging

class Event:
    """
    Base class for any in-game event, includes basic event attributes.
    """

    def __init__(self, event_category: str, event_type: str, action: str, source: str, target: str, damage_value: int = 0) -> None:
        # logging.debug("Initializing Event")
        self.event_category = event_category  # 'incoming', 'outgoing', 'notification'
        self.event_type = event_type          # 'combat', 'skill', 'avoidance'
        self.action = action                  # Normalized action verb, e.g., 'punch'
        self.source = source                  # Player or entity attacking
        self.target = target                  # Player or entity being attacked
        self.damage_value = damage_value      # Numeric value of damage if available

    def __repr__(self) -> str:
        # logging.debug("Generating Event representation")
        return f"{self.event_category.capitalize()} {self.event_type.capitalize()}: source={self.source}, action={self.action}, target={self.target}, damage={self.damage_value}"


class CombatEvent(Event):
    """
    Represents a combat-related event.
    """
    def __init__(self, event_category: str, action: str, source: str, target: str, damage_value: int) -> None:
        # logging.debug("Creating CombatEvent")
        super().__init__(event_category, 'combat', action, source, target, damage_value)


class SkillEvent(Event):
    """
    Represents a skill-related event.
    """
    def __init__(self, event_category: str, action: str, source: str, target: str, damage_value: int) -> None:
        # logging.debug("Creating SkillEvent")
        super().__init__(event_category, 'skill', action, source, target, damage_value)


class AvoidanceEvent(Event):
    """
    Represents an avoidance event (e.g., dodge, block).
    """
    def __init__(self, event_category: str, action: str, source: str, target: str, avoidance_type: str) -> None:
        # logging.debug("Creating AvoidanceEvent")
        super().__init__(event_category, 'avoidance', action, source, target)
        self.avoidance_type = avoidance_type  # e.g., 'miss', 'dodge', 'absorb'

    def __repr__(self) -> str:
        # logging.debug("Generating AvoidanceEvent representation")
        return f"{self.event_category.capitalize()} {self.event_type.capitalize()}: source={self.source}, action={self.action}, target={self.target}, avoidance={self.avoidance_type}"
