import re
from src.parsers.log_parser import LogParser

class CombatEvent:
    """
    Represents a combat event, storing details like damage type, target, and damage value.
    """
    def __init__(self, event_type, damage_type, source, target, damage_value):
        self.event_type = event_type  # e.g., 'incoming', 'outgoing'
        self.damage_type = damage_type  # e.g., 'slash', 'hit'
        self.source = source  # e.g., player or NPC
        self.target = target  # e.g., player or NPC
        self.damage_value = int(damage_value)  # Numeric value of the damage

    def __repr__(self):
        return f"{self.event_type} event: {self.source} {self.damage_type} {self.target} for {self.damage_value} damage."


class ChatLogParser(LogParser):
    """
    A class for parsing chat log files and generating combat events.
    """

    def __init__(self, log_file_path):
        super().__init__(log_file_path)
        self.damage_types_outgoing = ["crush", "punch", "slash", "pierce", "hit"]
        self.damage_types_incoming = ["crushes", "punches", "slashes", "pierces", "hits", "gores", "mauls", "bites",
                                      "stings", "claws", "slices", "smashes", "rends", "slams", "burns", "frenzies on"]
        self.player_outgoing_regex = self.build_outgoing_regex()
        self.player_incoming_regex = self.build_incoming_regex()
        self.events = []  # List to store generated events

    def build_outgoing_regex(self):
        """
        Build the regex for parsing outgoing damage events.
        """
        damage_types = "|".join(self.damage_types_outgoing)
        return re.compile(rf"You ({damage_types}) (\w+( \w+)?) for (\d+) point(?:s)? of damage.")

    def build_incoming_regex(self):
        """
        Build the regex for parsing incoming damage events.
        """
        damage_types = "|".join(self.damage_types_incoming)
        return re.compile(rf"(\w+( \w+)?) ({damage_types}) YOU for (\d+) point(?:s)? of damage.")

    def parse_line(self, line):
        """
        Parses a single line from the chat log and generates events for combat actions.
        """
        # Outgoing damage (player hits NPC)
        outgoing_match = self.player_outgoing_regex.search(line)
        if outgoing_match:
            damage_type = outgoing_match.group(1)
            monster_name = outgoing_match.group(2)
            damage_value = outgoing_match.group(4)
            self.create_event('outgoing', damage_type, 'Player', monster_name, damage_value)
            return

        # Incoming damage (NPC hits player)
        incoming_match = self.player_incoming_regex.search(line)
        if incoming_match:
            monster_name = incoming_match.group(1)
            damage_type = incoming_match.group(3)
            damage_value = incoming_match.group(4)
            self.create_event('incoming', damage_type, monster_name, 'Player', damage_value)
            return

    def create_event(self, event_type, damage_type, source, target, damage_value):
        """
        Creates a combat event and stores it in the event list for future use.
        """
        event = CombatEvent(event_type, damage_type, source, target, damage_value)
        self.events.append(event)  # Add the event to the list
        print(f"Event created: {event}")

    def monitor(self):
        """
        Monitor the chat log in real-time for new lines and generates events.
        """
        new_lines = self.read_lines()  # Only reads new lines since last check
        if not new_lines:
            print("No new lines to process.")
        for line in new_lines:
            self.parse_line(line)
