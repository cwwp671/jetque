# jetque/src/animations/animation_controller.py

import logging
from PyQt6.QtCore import QObject, Qt, pyqtSignal
from src.animations.animation_factory import AnimationFactory
from src.animations.text_label import TextLabel

class AnimationController(QObject):
    """Controller to manage animations."""

    animation_finished = pyqtSignal(QObject)

    def __init__(self, parent_widget, config):
        super().__init__()
        self.parent_widget = parent_widget
        self.config = config
        self.active_animations = []

    def play_animation(self, text, animation_type, behavior, direction):
        """Create and play a new animation."""
        # Bump existing animations of the same type to prevent overlap
        bump_percentage = 10.0
        for animation in self.active_animations:
            if animation.type == animation_type:
                animation.bump_elapsed_time(bump_percentage)

        # Update the config with the specified animation settings
        self.config['text']['content'] = text
        self.config['text']['animation']['type'] = animation_type
        self.config['text']['animation']['behavior'] = behavior
        self.config['text']['animation']['direction'] = direction

        text_label = TextLabel(self.parent_widget, self.config)
        text_label.show()

        animation = AnimationFactory.create_animation(text_label, self.config)
        logging.debug(
            f"Created {self.config['text']['animation'].get('type', 'Unknown')} animation."
        )

        animation.finished.connect(self.on_animation_finished, Qt.ConnectionType.QueuedConnection)
        logging.debug("Connected finished signal.")
        animation.play()
        self.active_animations.append(animation)
        logging.debug("Animation started and added to active animations.")

    def on_animation_finished(self, animation):
        """Handle the cleanup after an animation finishes."""
        if animation in self.active_animations:
            self.active_animations.remove(animation)
            logging.debug("Animation removed from active animations.")
        else:
            logging.warning("Finished animation not found in active animations.")
