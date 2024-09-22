import re
from src.parsers.log_parser import LogParser

class CombatEvent:
    """
    Represents a combat event, storing details like damage type, target, and damage value.
    """
    def __init__(self, event_type: str, damage_type: str, source: str, target: str, damage_value: int) -> None:
        self.event_type = event_type  # e.g., 'incoming', 'outgoing'
        self.damage_type = damage_type  # e.g., 'slash', 'hit'
        self.source = source  # e.g., player or NPC
        self.target = target  # e.g., player or NPC
        self.damage_value = damage_value  # Numeric value of the damage

    def __repr__(self) -> str:
        return (
            f"{self.event_type} event: {self.source} {self.damage_type} {self.target} "
            f"for {self.damage_value} damage."
        )


class ChatLogParser(LogParser):
    """
    A class for parsing chat log files and generating combat events.
    """

    DAMAGE_TYPES_OUTGOING = [
        "crush", "punch", "slash", "pierce", "hit"
    ]
    DAMAGE_TYPES_INCOMING = [
        "crushes", "punches", "slashes", "pierces", "hits", "gores", "mauls", "bites",
        "stings", "claws", "slices", "smashes", "rends", "slams", "burns", "frenzies on"
    ]

    def __init__(self, log_file_path: str) -> None:
        super().__init__(log_file_path)
        self.player_outgoing_regex = self.build_combat_regex(self.DAMAGE_TYPES_OUTGOING, outgoing=True)
        self.player_incoming_regex = self.build_combat_regex(self.DAMAGE_TYPES_INCOMING, outgoing=False)
        self.events = []  # List to store generated events

    def parse_log(self) -> None:
        """
        The required method from the parent LogParser class.
        This method processes the log to generate combat events.
        """
        self.reset_log_state()
        lines = self.read_log()
        for line in lines:
            self.parse_combat_line(line)

    @staticmethod
    def build_combat_regex(damage_types: list, outgoing: bool = True) -> re.Pattern:
        """
        Build the regex for parsing combat events based on whether it's outgoing or incoming.
        """
        damage_pattern = "|".join(damage_types)
        if outgoing:
            return re.compile(rf"You ({damage_pattern}) (\w+(\s\w+)?) for (\d+) points? of damage.")
        return re.compile(rf"(\w+(\s\w+)?) ({damage_pattern}) YOU for (\d+) points? of damage.")

    @staticmethod
    def safe_int(value: str) -> int:
        """
        Safely convert a string to an integer, returning 0 if the conversion fails.
        """
        try:
            return int(value)
        except ValueError:
            print(f"Warning: Could not convert '{value}' to an integer. Defaulting to 0.")
            return 0

    def parse_combat_line(self, line: str) -> None:
        """
        Parses a single line from the chat log and generates events for combat actions.
        """
        # Outgoing damage (player hits NPC)
        outgoing_match = self.player_outgoing_regex.search(line)
        if outgoing_match:
            damage_type = outgoing_match.group(1)
            monster_name = outgoing_match.group(2)
            damage_value = self.safe_int(outgoing_match.group(4))  # Ensure damage_value is an int
            self.create_event('outgoing', damage_type, 'Player', monster_name, damage_value)
            return

        # Incoming damage (NPC hits player)
        incoming_match = self.player_incoming_regex.search(line)
        if incoming_match:
            monster_name = incoming_match.group(1)
            damage_type = incoming_match.group(3)
            damage_value = self.safe_int(incoming_match.group(4))  # Ensure damage_value is an int
            self.create_event('incoming', damage_type, monster_name, 'Player', damage_value)
            return

    def create_event(self, event_type: str, damage_type: str, source: str, target: str, damage_value: int) -> None:
        """
        Creates a combat event and stores it in the event list for future use.
        """
        event = CombatEvent(event_type, damage_type, source, target, damage_value)
        self.events.append(event)  # Add the event to the list
        print(f"Event created: {event}")

    def monitor_log(self) -> None:
        """
        Continuously monitor the chat log in real-time and generate combat events.
        """
        while True:
            new_lines = self.read_log()  # Read only new lines
            if not new_lines:
                print("No new lines to process.")
            for line in new_lines:
                self.parse_combat_line(line)
