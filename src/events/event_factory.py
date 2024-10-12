# jetque/src/parsers/event_factory.py

import re
import logging
from src.events.event import CombatEvent, SkillEvent, AvoidanceEvent

class EventFactory:
    """
    Responsible for creating event objects based on log lines.
    """

    # Define action verbs for combat, skill, and avoidance
    COMBAT = (
        r'crush(?:es)?|punch(?:es)?|slash(?:es)?|pierce(?:s)?|hit(?:s)?|gore(?:s)?|'
        r'maul(?:s)?|bite(?:s)?|sting(?:s)?'
    )
    SKILL = r'backstab(?:s)?|kick(?:s)?|bash(?:es)?|strike(?:s)?'
    AVOIDANCE = r'dodge(?:s)?|block(?:s)?|parr(?:y|ies)|riposte(?:s)?|miss(?:es)?|magical skin absorbs the blow'

    # Compile regex patterns for outgoing events
    OUTGOING_COMBAT = re.compile(
        rf'You (?P<action>{COMBAT}) (?P<target>[\w\s]+?) for (?P<damage>\d+) points? of damage\.'
    )
    OUTGOING_SKILL = re.compile(
        rf'You (?P<action>{SKILL}) (?P<target>[\w\s]+?) for (?P<damage>\d+) points? of damage\.'
    )
    OUTGOING_AVOIDANCE = re.compile(
        rf'You try to (?P<action>{COMBAT}|{SKILL}) (?P<target>[\w\s]+?), but(?: (?P<entity>[\w\s\']+?))? (?P<avoidance>{AVOIDANCE})!'
    )

    # Compile regex patterns for incoming events
    INCOMING_COMBAT = re.compile(
        rf'(?P<entity>[\w\s]+?) (?P<action>{COMBAT}) YOU for (?P<damage>\d+) points? of damage\.'
    )
    INCOMING_SKILL = re.compile(
        rf'(?P<entity>[\w\s]+?) (?P<action>{SKILL}) YOU for (?P<damage>\d+) points? of damage\.'
    )
    INCOMING_AVOIDANCE = re.compile(
        rf'(?P<entity>[\w\s\']+?) tries to (?P<action>{COMBAT}|{SKILL}) YOU, but(?: YOU)? (?P<avoidance>{AVOIDANCE})!'
    )

    # Mapping for normalization
    NORMALIZATION_MAPPING = {
        # Combat actions
        'crushes': 'crush',
        'crush': 'crush',
        'punches': 'punch',
        'punch': 'punch',
        'slashes': 'slash',
        'slash': 'slash',
        'pierces': 'pierce',
        'pierce': 'pierce',
        'hits': 'hit',
        'hit': 'hit',
        'gores': 'gore',
        'gore': 'gore',
        'mauls': 'maul',
        'maul': 'maul',
        'bites': 'bite',
        'bite': 'bite',
        'stings': 'sting',
        'sting': 'sting',
        # Skill actions
        'backstabs': 'backstab',
        'backstab': 'backstab',
        'kicks': 'kick',
        'kick': 'kick',
        'bashes': 'bash',
        'bash': 'bash',
        'strikes': 'strike',
        'strike': 'strike',
        # Avoidance actions
        'dodges': 'dodge',
        'dodge': 'dodge',
        'blocks': 'block',
        'block': 'block',
        'parries': 'parry',
        'parry': 'parry',
        'ripostes': 'riposte',
        'riposte': 'riposte',
        'misses': 'miss',
        'miss': 'miss',
        'magical skin absorbs the blow': 'absorb',
        'absorb': 'absorb',
    }

    @staticmethod
    def normalize_action(action: str) -> str:
        """
        Normalize action verbs to their base forms.
        """
        action = action.lower().strip()
        normalized_action = EventFactory.NORMALIZATION_MAPPING.get(action)
        if normalized_action:
            return normalized_action
        else:
            # Attempt to handle cases not explicitly mapped
            # For example, removing trailing 'es' or 's' if present
            if action.endswith('es') and action[:-2] in EventFactory.NORMALIZATION_MAPPING:
                return EventFactory.NORMALIZATION_MAPPING[action[:-2]]
            elif action.endswith('s') and action[:-1] in EventFactory.NORMALIZATION_MAPPING:
                return EventFactory.NORMALIZATION_MAPPING[action[:-1]]
            else:
                logging.warning(f"Unrecognized action type: '{action}'. Returning original value.")
                return action  # or return 'unknown' as a default

    @staticmethod
    def create_event_from_line(line: str):
        """
        Create the appropriate event based on the log line.
        Uses regex to identify event types and instantiate the corresponding event class.
        """
        try:
            # Outgoing Combat
            match = EventFactory.OUTGOING_COMBAT.search(line)
            if match:
                logging.debug(f"Outgoing combat match: {line}")
                action = EventFactory.normalize_action(match.group('action'))
                return CombatEvent(
                    'outgoing',
                    action,
                    'Player',
                    match.group('target'),
                    int(match.group('damage'))
                )

            # Outgoing Skill
            match = EventFactory.OUTGOING_SKILL.search(line)
            if match:
                logging.debug(f"Outgoing skill match: {line}")
                action = EventFactory.normalize_action(match.group('action'))
                return SkillEvent(
                    'outgoing',
                    action,
                    'Player',
                    match.group('target'),
                    int(match.group('damage'))
                )

            # Outgoing Avoidance
            match = EventFactory.OUTGOING_AVOIDANCE.search(line)
            if match:
                logging.debug(f"Outgoing avoidance match: {line}")
                action = EventFactory.normalize_action(match.group('action'))
                avoidance = match.group('avoidance')
                normalized_avoidance = EventFactory.normalize_action(avoidance)
                return AvoidanceEvent(
                    'outgoing',
                    action,
                    'Player',
                    match.group('target'),
                    normalized_avoidance
                )

            # Incoming Combat
            match = EventFactory.INCOMING_COMBAT.search(line)
            if match:
                entity = match.group('entity').strip()  # Strip spaces
                if entity.startswith('A ') or entity.startswith('An '):
                    entity_name = entity.lower()
                else:
                    entity_name = entity
                logging.debug(f"Incoming combat match: {line}")
                action = EventFactory.normalize_action(match.group('action'))
                return CombatEvent(
                    'incoming',
                    action,
                    entity_name,
                    'Player',
                    int(match.group('damage'))
                )

            # Incoming Skill
            match = EventFactory.INCOMING_SKILL.search(line)
            if match:
                entity = match.group('entity').strip()  # Strip spaces
                if entity.startswith('A ') or entity.startswith('An '):
                    entity_name = entity.lower()
                else:
                    entity_name = entity
                logging.debug(f"Incoming skill match: {line}")
                action = EventFactory.normalize_action(match.group('action'))
                return SkillEvent(
                    'incoming',
                    action,
                    entity_name,
                    'Player',
                    int(match.group('damage'))
                )

            # Incoming Avoidance
            match = EventFactory.INCOMING_AVOIDANCE.search(line)
            if match:
                entity = match.group('entity').strip()  # Strip spaces
                if entity.startswith('A ') or entity.startswith('An '):
                    entity_name = entity.lower()
                else:
                    entity_name = entity
                logging.debug(f"Incoming avoidance match: {line}")
                action = EventFactory.normalize_action(match.group('action'))
                avoidance = match.group('avoidance')
                normalized_avoidance = EventFactory.normalize_action(avoidance)
                return AvoidanceEvent(
                    'incoming',
                    action,
                    entity_name,
                    'Player',
                    normalized_avoidance
                )

            logging.debug(f"No matching event found for line: {line}")
            return None

        except Exception as e:
            logging.error(f"Error parsing line: {line} - {e}")
            return None
