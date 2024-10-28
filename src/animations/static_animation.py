# jetque/src/animations/static_animation.py
import logging
from typing import Any, Dict

from PyQt6.QtWidgets import QGraphicsOpacityEffect
from src.animations.animation import Animation


class StaticAnimation(Animation):
    """
    Implements a static animation by displaying a text label for a fixed duration
    with an optional fade-out opacity effect.

    Attributes:
        DEFAULT_DURATION (float): Default duration for the static animation in seconds.
        MIN_OPACITY (float): Minimum opacity value.
        MAX_OPACITY (float): Maximum opacity value.
        FADE_START_PERCENTAGE (float): Percentage of duration to start fading opacity.
        duration (float): Duration for which the animation runs.
        behavior (str): Placeholder for animation behavior.
        direction (str): Placeholder for animation direction.
        ms_per_frame (int): Milliseconds per frame for the animation.
        delta_time (float): Time increment per frame in seconds.
        elapsed_time (float): Total elapsed time since the animation started.
        opacity_effect (QGraphicsOpacityEffect): Opacity effect applied to the text label.
    """

    DEFAULT_DURATION: float = 3.15
    MIN_OPACITY: float = 0.0
    MAX_OPACITY: float = 1.0
    FADE_START_PERCENTAGE: float = 0.5

    def __init__(self, text_label: Any, config: Dict[str, Any]) -> None:
        """
        Initialize the StaticAnimation instance with an optional fade-out effect.

        Args:
            text_label (Any): The label to display during the animation.
            config (Dict[str, Any]): Configuration settings for the animation.

        Raises:
            KeyError: If 'ms_per_frame' is missing in the configuration.
        """
        super().__init__(text_label, config)
        self.duration: float = self.DEFAULT_DURATION
        self.behavior: str = 'None'
        self.direction: str = 'None'  # TODO: Implement Up/Down/Right/Left Collision
        self.ms_per_frame: int = self.config['text']['animation']['ms_per_frame']
        self.delta_time: float = self.ms_per_frame / 1000.0
        self.elapsed_time: float = 0.0
        self.opacity_effect: QGraphicsOpacityEffect = QGraphicsOpacityEffect()
        self.text_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(self.MAX_OPACITY)
        self.start_in_center()

        logging.debug("StaticAnimation initialized with duration: %.2f seconds.", self.duration)

    def animate(self) -> None:
        """
        Perform the static animation by incrementing elapsed time and updating opacity.
        Stops the animation when the duration is reached.
        """
        try:
            self.elapsed_time += self.delta_time
            progress: float = min(1.0, self.elapsed_time / self.duration)
            logging.debug("Elapsed time: %.2f seconds. Progress: %.2f%%", self.elapsed_time, progress * 100)
            opacity: float = self._calculate_opacity(progress)
            self.opacity_effect.setOpacity(opacity)
            logging.debug("Updated opacity to: %.2f", opacity)

            if self.elapsed_time >= self.duration:
                logging.info("Animation duration reached. Stopping animation.")
                self.stop()
        except Exception as e:
            logging.exception("An error occurred during animation: %s", e)

    def stop(self) -> None:
        """
        Stop the animation and delete the text label.
        """
        try:
            super().stop()
            self.text_label.deleteLater()
            logging.info("StaticAnimation stopped and label deleted.")
        except Exception as e:
            logging.exception("An error occurred while stopping the animation: %s", e)

    def _calculate_opacity(self, progress: float) -> float:
        """
        Calculate the opacity based on the progress of the animation to create a fade-out effect.
        The opacity remains at MAX_OPACITY until halfway through the duration, then fades to MIN_OPACITY.

        Args:
            progress (float): The progress of the animation (0.0 to 1.0).

        Returns:
            float: The calculated opacity value.
        """
        try:
            if progress < self.FADE_START_PERCENTAGE:
                opacity: float = self.MAX_OPACITY
            else:
                fade_progress: float = (progress - self.FADE_START_PERCENTAGE) / (1.0 - self.FADE_START_PERCENTAGE)
                opacity = self.MAX_OPACITY - (self.MAX_OPACITY - self.MIN_OPACITY) * fade_progress

            opacity = max(self.MIN_OPACITY, min(self.MAX_OPACITY, opacity))
            return opacity
        except Exception as e:
            logging.error(f"Exception in _calculate_opacity(): {e}")
            return self.MAX_OPACITY
