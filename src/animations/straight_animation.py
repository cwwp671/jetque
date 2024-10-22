# jetque/src/animations/straight_animation.py

import logging
from src.animations.animation import Animation

class StraightAnimation(Animation):
    """Implements straight scroll (Up, Down) animation."""

    DEFAULT_MOVE_DISTANCE = 40  # Default movement distance

    def __init__(self, text_label, config):
        super().__init__(text_label, config)
        animation_config = config['text']['animation']
        self.behavior = None
        self.direction = animation_config.get('direction', 'Up')
        self.move_distance = animation_config.get('move_distance', self.DEFAULT_MOVE_DISTANCE)

        self.start_x = text_label.x()
        self.start_y = text_label.y()

        self.ms_per_frame = self.config['text']['animation']['ms_per_frame']
        self.delta_time = self.ms_per_frame / 1000.0

        logging.debug(
            f"StraightAnimation initialized with direction: {self.direction}, "
            f"move_distance: {self.move_distance}"
        )

    def animate(self):
        """Animate the text straight in the specified direction."""
        self.elapsed_time += self.delta_time
        progress = min(1, self.elapsed_time / self.duration)
        distance = self.move_distance * progress

        if self.direction == "Up":
            new_y = self.start_y - distance
        else:  # Down
            new_y = self.start_y + distance

        self.text_label.move(self.start_x, int(new_y))

        if self.elapsed_time >= self.duration:
            logging.debug("Animation duration reached. Stopping animation.")
            self.stop()

    def stop(self):
        """Stop the animation and delete the text label."""
        super().stop()
        self.text_label.deleteLater()
        logging.debug("StraightAnimation stopped and label deleted.")
