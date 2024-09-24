import unittest
from unittest.mock import MagicMock
from src.events.event_handler import EventHandler
from src.events.event import CombatEvent, SkillEvent, AvoidanceEvent


class TestEventHandler(unittest.TestCase):

    def setUp(self) -> None:
        """
        Set up a fresh instance of EventHandler before each test.
        """
        self.event_handler = EventHandler()

    def test_add_event(self):
        """
        Test that events are correctly added to the event queue.
        """
        combat_event = CombatEvent('outgoing', 'Player', 'a goblin', 50)
        self.event_handler.add_event(combat_event)

        self.assertEqual(len(self.event_handler.event_queue), 1)
        self.assertEqual(self.event_handler.event_queue[0], combat_event)

    def test_process_event_queue(self):
        """
        Test that events in the queue are processed and dispatched.
        """
        combat_event = CombatEvent('outgoing', 'Player', 'a goblin', 50)
        skill_event = SkillEvent('outgoing', 'Player', 'a rat', 60)
        avoidance_event = AvoidanceEvent('incoming', 'a goblin', 'Player')

        # Mocking the display methods, so we don't actually print anything
        self.event_handler.display_combat_event = MagicMock()
        self.event_handler.display_skill_event = MagicMock()
        self.event_handler.display_avoidance_event = MagicMock()

        # Add events to the queue
        self.event_handler.add_event(combat_event)
        self.event_handler.add_event(skill_event)
        self.event_handler.add_event(avoidance_event)

        # Process the event queue
        self.event_handler.process_event_queue()

        # Ensure that the queue is empty after processing
        self.assertEqual(len(self.event_handler.event_queue), 0)

        # Ensure each event was dispatched to the correct method
        self.event_handler.display_combat_event.assert_called_once_with(combat_event)
        self.event_handler.display_skill_event.assert_called_once_with(skill_event)
        self.event_handler.display_avoidance_event.assert_called_once_with(avoidance_event)

    def test_dispatch_combat_event(self):
        """
        Test that a combat event is dispatched correctly.
        """
        combat_event = CombatEvent('outgoing', 'Player', 'a goblin', 50)
        self.event_handler.display_combat_event = MagicMock()

        self.event_handler.dispatch_event(combat_event)
        self.event_handler.display_combat_event.assert_called_once_with(combat_event)

    def test_dispatch_skill_event(self):
        """
        Test that a skill event is dispatched correctly.
        """
        skill_event = SkillEvent('outgoing', 'Player', 'a rat', 60)
        self.event_handler.display_skill_event = MagicMock()

        self.event_handler.dispatch_event(skill_event)
        self.event_handler.display_skill_event.assert_called_once_with(skill_event)

    def test_dispatch_avoidance_event(self):
        """
        Test that an avoidance event is dispatched correctly.
        """
        avoidance_event = AvoidanceEvent('incoming', 'a goblin', 'Player')
        self.event_handler.display_avoidance_event = MagicMock()

        self.event_handler.dispatch_event(avoidance_event)
        self.event_handler.display_avoidance_event.assert_called_once_with(avoidance_event)


if __name__ == '__main__':
    unittest.main()
