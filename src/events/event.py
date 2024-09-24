class Event:
    """
    Base class for any in-game event, includes basic event attributes.
    """

    def __init__(self, event_category: str, event_type: str, source: str, target: str, damage_value: int = 0) -> None:
        self.event_category = event_category  # 'incoming', 'outgoing', 'notification'
        self.event_type = event_type  # 'combat', 'skill', 'avoidance'
        self.source = source  # Player or entity attacking
        self.target = target  # Player or entity being attacked
        self.damage_value = damage_value  # Numeric value of damage if available

    def __repr__(self) -> str:
        return f"{self.event_category.capitalize()} {self.event_type} " \
               f"event: {self.source} -> {self.target} for {self.damage_value} damage."


class CombatEvent(Event):
    """
    Represents a combat-related event.
    """
    def __init__(self, event_category: str, source: str, target: str, damage_value: int) -> None:
        super().__init__(event_category, 'combat', source, target, damage_value)


class SkillEvent(Event):
    """
    Represents a skill-related event.
    """
    def __init__(self, event_category: str, source: str, target: str, damage_value: int) -> None:
        super().__init__(event_category, 'skill', source, target, damage_value)


class AvoidanceEvent(Event):
    """
    Represents an avoidance event (e.g., dodge, block).
    """
    def __init__(self, event_category: str, source: str, target: str) -> None:
        super().__init__(event_category, 'avoidance', source, target)
