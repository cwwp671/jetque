# jetque/src/animations/static_animation.py

import logging
from src.animations.animation import Animation

class StaticAnimation(Animation):
    """Implements static animation."""

    DEFAULT_DURATION = 3.15  # Static display time

    def __init__(self, text_label, config):
        super().__init__(text_label, config)
        self.duration = self.DEFAULT_DURATION

        self.ms_per_frame = self.config['text']['animation']['ms_per_frame']
        self.delta_time = self.ms_per_frame / 1000.0

        logging.debug("StaticAnimation initialized.")

    def animate(self):
        """Static animation does not move; waits for duration to expire."""
        self.elapsed_time += self.delta_time
        if self.elapsed_time >= self.duration:
            logging.debug("Animation duration reached. Stopping animation.")
            self.stop()

    def stop(self):
        """Stop the animation and delete the text label."""
        super().stop()
        self.text_label.deleteLater()
        logging.debug("StaticAnimation stopped and label deleted.")
