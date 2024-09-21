import re
from src.parsers.log_parser import LogParser

class ChatLogParser(LogParser):
    """
    A class for parsing chat log files for specific combat events.
    """

    # Compile regex patterns for player outgoing and incoming damage
    outgoing_damage_greater_than_one_regex = re.compile(
        r"You (crush|punch|slash|pierce|hit) (\w+(?: \w+)*) for (\d+) points of damage."
    )

    outgoing_damage_equal_one_regex = re.compile(
        r"You (crush|punch|slash|pierce|hit) (\w+(?: \w+)*) for 1 point of damage."
    )

    incoming_damage_greater_than_one_regex = re.compile(
        r"(\w+(?: \w+)*) (crushes|punches|slashes|pierces|hits|gores|mauls|bites|stings|claws|slices|smashes|rends|slams|burns|frenzies on) YOU for (\d+) points of damage."
    )

    incoming_damage_equal_one_regex = re.compile(
        r"(\w+(?: \w+)*) (crushes|punches|slashes|pierces|hits|gores|mauls|bites|stings|claws|slices|smashes|rends|slams|burns|frenzies on) YOU for 1 point of damage."
    )

    def parse_line(self, line):
        """
        Parses a single line from the chat log for basic combat damage events.

        :param line: The line to parse.
        """
        # Check for outgoing damage (greater than one)
        outgoing_match = self.outgoing_damage_greater_than_one_regex.search(line)
        if outgoing_match:
            damage_type, monster_name, damage = outgoing_match.groups()
            print(f"Outgoing Damage: You {damage_type} {monster_name} for {damage} points of damage.")
            return

        # Check for outgoing damage (exactly one point)
        outgoing_match_one = self.outgoing_damage_equal_one_regex.search(line)
        if outgoing_match_one:
            damage_type, monster_name = outgoing_match_one.groups()
            print(f"Outgoing Damage: You {damage_type} {monster_name} for 1 point of damage.")
            return

        # Check for incoming damage (greater than one)
        incoming_match = self.incoming_damage_greater_than_one_regex.search(line)
        if incoming_match:
            monster_name, damage_type, damage = incoming_match.groups()
            print(f"Incoming Damage: {monster_name} {damage_type} YOU for {damage} points of damage.")
            return

        # Check for incoming damage (exactly one point)
        incoming_match_one = self.incoming_damage_equal_one_regex.search(line)
        if incoming_match_one:
            monster_name, damage_type = incoming_match_one.groups()
            print(f"Incoming Damage: {monster_name} {damage_type} YOU for 1 point of damage.")
            return

    def monitor(self):
        """
        Monitor the chat log in real-time for new lines.
        """
        lines = self.read_lines()  # Inherited from LogParser
        for line in lines:
            self.parse_line(line)
