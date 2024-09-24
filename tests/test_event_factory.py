import unittest
from src.events.event_factory import EventFactory
from src.events.event import CombatEvent, SkillEvent, AvoidanceEvent

class TestEventFactory(unittest.TestCase):
    def assert_event(self, event, event_class, category, source, target, damage=None):
        self.assertIsInstance(event, event_class)
        self.assertEqual(event.event_category, category)
        self.assertEqual(event.source, source)
        self.assertEqual(event.target, target)
        if damage is not None:
            self.assertEqual(event.damage_value, damage)

    def test_create_outgoing_combat_event(self):
        log_line = "You crush a goblin for 50 points of damage."
        event = EventFactory.create_event_from_line(log_line)
        self.assert_event(event, CombatEvent, 'outgoing', 'Player', 'a goblin', 50)

    def test_create_outgoing_skill_event(self):
        log_line = "You backstab a rat for 60 points of damage."
        event = EventFactory.create_event_from_line(log_line)
        self.assert_event(event, SkillEvent, 'outgoing', 'Player', 'a rat', 60)

    def test_create_outgoing_avoidance_event(self):
        log_line = "You try to crush a goblin, but a goblin dodges!"
        event = EventFactory.create_event_from_line(log_line)
        self.assert_event(event, AvoidanceEvent, 'outgoing', 'Player', 'a goblin')

    def test_create_incoming_combat_event(self):
        log_line = "A goblin crushes YOU for 30 points of damage."
        event = EventFactory.create_event_from_line(log_line)
        self.assert_event(event, CombatEvent, 'incoming', 'A goblin', 'Player', 30)

    def test_create_incoming_skill_event(self):
        log_line = "A goblin backstabs YOU for 40 points of damage."
        event = EventFactory.create_event_from_line(log_line)
        self.assert_event(event, SkillEvent, 'incoming', 'A goblin', 'Player', 40)

    def test_create_incoming_avoidance_event(self):
        log_line = "A goblin tries to crush YOU, but YOU dodge!"
        event = EventFactory.create_event_from_line(log_line)
        self.assert_event(event, AvoidanceEvent, 'incoming', 'A goblin', 'Player')

    def test_no_event_created_for_irrelevant_line(self):
        log_line = "You say, 'Hello!'"
        event = EventFactory.create_event_from_line(log_line)
        self.assertIsNone(event)
