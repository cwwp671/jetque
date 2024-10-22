# jetque/src/animations/animation_controller.py

import logging
from PyQt6.QtCore import QObject, Qt, pyqtSignal, QTimer
from src.animations.animation_factory import AnimationFactory
from src.animations.text_label import TextLabel
from PyQt6.QtWidgets import QLabel

class AnimationController(QObject):
    """Controller to manage animations."""

    animation_finished = pyqtSignal(QObject)

    def __init__(self, parent_widget, config):
        super().__init__()
        self.parent_widget = parent_widget
        self.config = config
        self.active_animations = []
        self.collision_timer = QTimer(self)
        self.collision_timer.setInterval(16)
        self.collision_timer.timeout.connect(self.perform_collision_detection)
        self.collision_timer.start()

    def play_animation(self, text, animation_type, behavior, direction):
        """Create and play a new animation."""
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

    def perform_collision_detection(self):
        """Perform real-time collision detection among all active animations."""

        for i, anim1 in enumerate(self.active_animations):
            for j, anim2 in enumerate(self.active_animations):
                if i >= j:
                    continue

                label1 = anim1.text_label
                label2 = anim2.text_label

                if self.are_overlapping(label1, label2):
                    logging.debug(f"Real-time overlap detected between '{label1.text()}' and '{label2.text()}'. Handling collision.")

                    self.handle_overlap(anim1, anim2)

    def are_overlapping(self, label1: QLabel, label2: QLabel) -> bool:
        """Determine if two QLabel widgets are overlapping based on their geometry."""
        rect1 = label1.geometry()
        rect2 = label2.geometry()

        overlap = rect1.intersects(rect2)
        logging.debug(f"Checking overlap between '{label1.text()}' and '{label2.text()}': {overlap}")
        return overlap

    def handle_overlap(self, anim1, anim2):
        """
        Handle collision by bumping the older animation forward based on elapsed_time.
        The animation with the higher elapsed_time is considered older.
        """
        if anim1.elapsed_time > anim2.elapsed_time:
            older_anim, newer_anim = anim1, anim2
        else:
            older_anim, newer_anim = anim2, anim1

        logging.debug(f"Older animation: '{older_anim.text_label.text()}' (elapsed_time: {older_anim.elapsed_time:.2f}s)")
        logging.debug(f"Newer animation: '{newer_anim.text_label.text()}' (elapsed_time: {newer_anim.elapsed_time:.2f}s)")

        if older_anim.elapsed_time >= 1.04 * newer_anim.elapsed_time:
            return

        bump_percentage = 0.06
        logging.debug(f"Bumping older animation '{older_anim.text_label.text()}' by {bump_percentage * 100}%.")
        older_anim.bump_elapsed_time(bump_percentage)

    def on_animation_finished(self, animation):
        """Handle the cleanup after an animation finishes."""
        if animation in self.active_animations:
            self.active_animations.remove(animation)
            logging.debug(f"Animation '{animation.text_label.text()}' removed from active animations.")
        else:
            logging.warning("Finished animation not found in active animations.")
