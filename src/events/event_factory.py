# jetque/src/parsers/event_factory.py

import re
import logging
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

    OUTGOING_COMBAT = re.compile(
        rf'You (?P<action>{COMBAT}) (?P<target>[\w\s]+?) for (?P<damage>\d+) points? of damage\.'
    )
    OUTGOING_SKILL = re.compile(
        rf'You (?P<action>{SKILL}) (?P<target>[\w\s]+?) for (?P<damage>\d+) points? of damage\.'
    )
    OUTGOING_AVOIDANCE = re.compile(
        rf'You try to (?P<action>{COMBAT}|{SKILL}) (?P<target>[\w\s]+?), but(?: (?P<entity>[\w\s\']+?))? (?P<avoidance>{AVOIDANCE})!'
    )

    INCOMING_COMBAT = re.compile(
        rf'(?P<entity>[\w\s]+?) (?P<action>{COMBAT}) YOU for (?P<damage>\d+) points? of damage\.'
    )
    INCOMING_SKILL = re.compile(
        rf'(?P<entity>[\w\s]+?) (?P<action>{SKILL}) YOU for (?P<damage>\d+) points? of damage\.'
    )
    INCOMING_AVOIDANCE = re.compile(
        rf'(?P<entity>[\w\s\']+?) tries to (?P<action>{COMBAT}|{SKILL}) YOU, but(?: YOU)? (?P<avoidance>{AVOIDANCE})!'
    )

    @staticmethod
    def create_event_from_line(line: str):
        """
        Create the appropriate event based on the log line.
        Uses regex to identify event types and instantiate the corresponding event class.
        """
        # Outgoing Combat
        match = EventFactory.OUTGOING_COMBAT.search(line)
        if match:
            logging.debug(f"Outgoing combat match: {line}")
            return CombatEvent(
                'outgoing',
                'Player',
                match.group('target'),
                int(match.group('damage'))
            )

        # Outgoing Skill
        match = EventFactory.OUTGOING_SKILL.search(line)
        if match:
            logging.debug(f"Outgoing skill match: {line}")
            return SkillEvent(
                'outgoing',
                'Player',
                match.group('target'),
                int(match.group('damage'))
            )

        # Outgoing Avoidance
        match = EventFactory.OUTGOING_AVOIDANCE.search(line)
        if match:
            logging.debug(f"Outgoing avoidance match: {line}")
            return AvoidanceEvent(
                'outgoing',
                'Player',
                match.group('target')
            )

        # Incoming Combat
        match = EventFactory.INCOMING_COMBAT.search(line)
        if match:
            entity_name = match.group('entity').capitalize()
            logging.debug(f"Incoming combat match: {line}")
            return CombatEvent(
                'incoming',
                entity_name,
                'Player',
                int(match.group('damage'))
            )

        # Incoming Skill
        match = EventFactory.INCOMING_SKILL.search(line)
        if match:
            entity_name = match.group('entity').capitalize()
            logging.debug(f"Incoming skill match: {line}")
            return SkillEvent(
                'incoming',
                entity_name,
                'Player',
                int(match.group('damage'))
            )

        # Incoming Avoidance
        match = EventFactory.INCOMING_AVOIDANCE.search(line)
        if match:
            entity_name = match.group('entity').capitalize()
            logging.debug(f"Incoming avoidance match: {line}")
            return AvoidanceEvent(
                'incoming',
                entity_name,
                'Player'
            )

        return None
