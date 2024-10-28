# jetque/src/animations/horizontal_animation.py

import logging
from typing import Any, Dict

from src.animations.animation import Animation


class HorizontalAnimation(Animation):
    """Implements horizontal animation for text labels."""

    def __init__(self, text_label: Any, config: Dict[str, Any]) -> None:
        """
        Initialize the HorizontalAnimation.

        Args:
            text_label (Any): The text label object to animate.
            config (Dict[str, Any]): Configuration dictionary for the animation.
        """
        super().__init__(text_label, config)
        try:
            animation_config: Dict[str, Any] = self.config['text']['animation']
            self.behavior: str = animation_config.get('behavior', 'Left')  # 'Left' or 'Right'
            self.duration: float = animation_config.get('duration', 1.5)  # Duration in seconds

            # Calculate starting and ending positions based on behavior
            self._calculate_start_positions()

            # Timing setup
            self.ms_per_frame: int = animation_config.get('ms_per_frame', 16)  # Default to ~60 FPS
            self.delta_time: float = self.ms_per_frame / 1000.0  # Convert ms to seconds

            # Initialize elapsed time
            self.elapsed_time: float = 0.0

            logging.debug(
                f"HorizontalAnimation initialized with behavior: {self.behavior}, "
                f"duration: {self.duration}s, ms_per_frame: {self.ms_per_frame}ms"
            )
        except KeyError as e:
            logging.error(f"Missing configuration key: {e}")
            raise

    def animate(self) -> None:
        """Animate the text horizontally based on behavior."""
        try:
            self.elapsed_time += self.delta_time
            progress: float = min(1.0, self.elapsed_time / self.duration)
            distance: float = self.end_x - self.start_x
            new_x: float = self.start_x + distance * progress

            self.text_label.move(int(new_x), int(self.start_y))
            logging.debug(f"Moving horizontally to x: {new_x:.2f}")

            if self.elapsed_time >= self.duration:
                logging.debug("Animation duration reached. Stopping animation.")
                self.stop()
        except Exception as e:
            logging.exception(f"Exception: {e}")
            self.stop()

    def stop(self) -> None:
        """Stop the animation and delete the text label."""
        try:
            super().stop()
            self.text_label.deleteLater()
            logging.debug("HorizontalAnimation stopped and label deleted.")
        except Exception as e:
            logging.exception(f"Exception: {e}")

    def _calculate_start_positions(self) -> None:
        """
        Calculate the starting and ending positions based on the behavior and parent widget's dimensions.
        """
        try:
            # Vertical position remains centered
            self.start_y: float = (self.overlay_height - self.label_height) / 2.0

            if self.behavior == 'Left':
                self.start_x = self.overlay_width - self.label_width
                self.end_x = 0.0
            elif self.behavior == 'Right':
                self.start_x = 0.0
                self.end_x = self.overlay_width - self.label_width
            else:
                logging.warning(f"Unknown behavior '{self.behavior}'. Defaulting to 'Left'.")
                self.start_x = self.overlay_width - self.label_width
                self.end_x = 0.0

            # Set the initial position and display the label
            self.text_label.move(int(self.start_x), int(self.start_y))
            self.text_label.show()

            logging.debug(
                f"HorizontalAnimation positions calculated: start=({self.start_x}, {self.start_y}), "
                f"end=({self.end_x}, {self.start_y})"
            )
        except Exception as e:
            logging.exception(f"Exception: {e}")
            raise
