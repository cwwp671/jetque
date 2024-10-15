# jetque/src/overlays/active_overlay.py

import logging
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel
from src.overlays.overlay import Overlay
from src.animations.animation_controller import AnimationController
from src.events.event import AvoidanceEvent

class ActiveOverlay(Overlay):
    def __init__(self, name, overlay_data):
        logging.debug("ActiveOverlay __init__: Start")
        super().__init__(name, overlay_data)
        logging.debug("ActiveOverlay __init__: After super().__init__")
        # Set window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        # Set attributes
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        # Make the window fully transparent
        self.setStyleSheet("background: transparent;")
        # Initialize label for displaying events
        self.animation_controller = AnimationController(self, overlay_data.get('config', {}))
        logging.debug("ActiveOverlay __init__: End")

    def display_event(self, event):
        # Determine the animation settings based on the event category
        if event.event_category == 'incoming':
            animation_type = 'Parabola'
            behavior = 'CurvedLeft'
            direction = 'Up'
            # Generate the message to display
            if isinstance(event, AvoidanceEvent):
                message = f"({event.source}) {event.avoidance_type}"
            else:
                message = f"({event.source}) {event.damage_value}"
        elif event.event_category == 'outgoing':
            animation_type = 'Parabola'
            behavior = 'CurvedRight'
            direction = 'Up'
            # Generate the message to display
            if isinstance(event, AvoidanceEvent):
                message = f"{event.avoidance_type} ({event.action})"
            else:
                message = f"{event.damage_value} ({event.action})"
        else:
            # Default settings
            animation_type = 'Static'
            behavior = 'Normal'
            direction = 'Up'
            message = str(event)

        # Play the animation
        self.animation_controller.play_animation(
            text=message,
            animation_type=animation_type,
            behavior=behavior,
            direction=direction
        )
