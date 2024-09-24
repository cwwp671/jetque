import re
from src.events.event import CombatEvent, SkillEvent, AvoidanceEvent

class EventFactory:
    """
    Responsible for creating event objects based on log lines.
    """

    COMBAT = (
        r'crush(?:es)?|punch(?:es)?|slash(?:es)?|pierce(?:s)?|hit(?:s)?|gore(?:s)?|'
        r'maul(?:s)?|bite(?:s)?|sting(?:s)?'
    )
    SKILL = r'backstab(?:s)?|kick(?:s)?|bash(?:es)?|strike(?:s)?'
    AVOIDANCE = r'dodge(?:s)?|block(?:s)?|parr(?:y|ies)|riposte(?:s)?|miss(?:es)?|magical skin absorbs the blow'

    OUTGOING_COMBAT = re.compile(rf'You ({COMBAT}) (\w+(\s\w+)?) for (\d+) points? of damage.')
    OUTGOING_SKILL = re.compile(rf'You ({SKILL}) (\w+(\s\w+)?) for (\d+) points? of damage.')
    OUTGOING_AVOIDANCE = re.compile(rf'You try to ({COMBAT}|{SKILL}) (\w+(\s\w+)?), but (\w+(\s\w+)?) ({AVOIDANCE})!')

    INCOMING_COMBAT = re.compile(rf'(\w+(\s\w+)?) ({COMBAT}) YOU for (\d+) points? of damage.')
    INCOMING_SKILL = re.compile(rf'(\w+(\s\w+)?) ({SKILL}) YOU for (\d+) points? of damage.')
    INCOMING_AVOIDANCE = re.compile(rf'(\w+(\s\w+)?) tries to ({COMBAT}|{SKILL}) YOU, but YOU ({AVOIDANCE})!')

    @staticmethod
    def create_event_from_line(line: str):
        """
        Create the appropriate event based on the log line.
        Uses regex to identify event types and instantiate the corresponding event class.
        """

        # Outgoing Combat
        match = EventFactory.OUTGOING_COMBAT.search(line)
        if match:
            return CombatEvent('outgoing', 'Player', match.group(2), int(match.group(4)))

        # Outgoing Skill
        match = EventFactory.OUTGOING_SKILL.search(line)
        if match:
            return SkillEvent('outgoing', 'Player', match.group(2), int(match.group(4)))

        # Outgoing Avoidance
        match = EventFactory.OUTGOING_AVOIDANCE.search(line)
        if match:
            return AvoidanceEvent('outgoing', 'Player', match.group(2))

        # Incoming Combat
        match = EventFactory.INCOMING_COMBAT.search(line)
        if match:
            entity_name = match.group(1)
            if line.startswith(entity_name.capitalize()):
                entity_name = entity_name.capitalize()
            return CombatEvent('incoming', entity_name, 'Player', int(match.group(4)))

        # Incoming Skill
        match = EventFactory.INCOMING_SKILL.search(line)
        if match:
            entity_name = match.group(1)
            if line.startswith(entity_name.capitalize()):
                entity_name = entity_name.capitalize()
            return SkillEvent('incoming', entity_name, 'Player', int(match.group(4)))

        # Incoming Avoidance
        match = EventFactory.INCOMING_AVOIDANCE.search(line)
        if match:
            entity_name = match.group(1)
            if line.startswith(entity_name.capitalize()):
                entity_name = entity_name.capitalize()
            return AvoidanceEvent('incoming', entity_name, 'Player')

        return None
