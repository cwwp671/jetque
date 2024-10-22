# jetque/src/animations/horizontal_animation.py

import logging
from src.animations.animation import Animation

class HorizontalAnimation(Animation):
    """Implements horizontal animation."""

    DEFAULT_MOVE_DISTANCE = 100  # Default distance to move

    def __init__(self, text_label, config):
        super().__init__(text_label, config)
        animation_config = config['text']['animation']
        self.behavior = None
        self.direction = animation_config.get('direction', 'Left')
        self.move_distance = animation_config.get('move_distance', self.DEFAULT_MOVE_DISTANCE)

        self.start_x = text_label.x()
        self.start_y = text_label.y()

        logging.debug(
            f"HorizontalAnimation initialized with direction: {self.direction}, "
            f"move_distance: {self.move_distance}"
        )

        self.ms_per_frame = self.config['text']['animation']['ms_per_frame']
        self.delta_time = self.ms_per_frame / 1000.0  # Convert ms to seconds
        logging.debug(
            f"HorizontalAnimation initialized with ms_per_frame: {self.ms_per_frame} ms, "
            f"delta_time: {self.delta_time} seconds."
        )

    def animate(self):
        """Animate the text horizontally based on direction."""
        self.elapsed_time += self.delta_time
        progress = min(1, self.elapsed_time / self.duration)
        distance = self.move_distance * progress

        if self.direction == "Left":
            new_x = self.start_x - distance
        else:  # Right
            new_x = self.start_x + distance

        self.text_label.move(int(new_x), self.start_y)
        logging.debug(f"Moving horizontally to x: {new_x: .2f}")

        if self.elapsed_time >= self.duration:
            logging.debug("Animation duration reached. Stopping animation.")
            self.stop()

    def stop(self):
        """Stop the animation and delete the text label."""
        super().stop()
        self.text_label.deleteLater()
        logging.debug("HorizontalAnimation stopped and label deleted.")
