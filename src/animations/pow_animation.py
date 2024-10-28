# jetque/src/animations/pow_animation.py
import logging
import random
from typing import Any, Dict

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsOpacityEffect

from src.animations.animation import Animation


class PowAnimation(Animation):
    """
    Implements Pow animation with scaling, display, and fade-out effects.

    Attributes:
        fade_in_time (float): Duration of the fade-in phase.
        display_time (float): Duration of the display phase.
        fade_out_time (float): Duration of the fade-out phase.
        text_delta (float): Scaling factor for the text during fade-in.
        jiggle_delay_time (float): Minimum delay between jiggle effects.
        jiggle_last_time (float): Timestamp of the last jiggle.
        font_size (int): Current font size of the text label.
        duration (float): Total duration of the animation.
        behavior (str): Behavior mode of the animation.
        direction (Any): Direction of the animation (unused).
        ms_per_frame (float): Milliseconds per frame for the animation.
        delta_time (float): Time increment per frame in seconds.
        opacity_effect (QGraphicsOpacityEffect): Opacity effect applied to the text label.
    """

    FADE_IN_TIME: float = 0.17
    DISPLAY_TIME: float = 1.5
    FADE_OUT_TIME: float = 0.5
    TEXT_DELTA: float = 0.7
    JIGGLE_DELAY_TIME: float = 0.05
    MIN_OPACITY: float = 0.0
    MAX_OPACITY: float = 1.0
    MIN_FONT_SIZE: int = 1
    JIGGLE_RANGE: int = 1

    def __init__(self, text_label: Any, config: Dict[str, Any]) -> None:
        """
        Initialize the PowAnimation with a text label and configuration.
        Args:
            text_label (Any): The label widget to animate.
            config (Dict[str, Any]): Configuration dictionary for the animation.
        """
        super().__init__(text_label, config)
        self.fade_in_time: float = self.FADE_IN_TIME
        self.display_time: float = self.DISPLAY_TIME
        self.fade_out_time: float = self.FADE_OUT_TIME
        self.text_delta: float = self.TEXT_DELTA
        self.jiggle_delay_time: float = self.JIGGLE_DELAY_TIME
        self.jiggle_last_time: float = 0.0
        self.font_size: int = text_label.font().pointSize()
        self.duration: float = self.fade_in_time + self.display_time + self.fade_out_time
        self.behavior: str = config['text']['animation'].get('behavior', 'Normal')
        self.direction: str = 'None'  # TODO: Implement Up/Down/Right/Left Collision
        self.ms_per_frame: float = self.config['text']['animation']['ms_per_frame']
        self.delta_time: float = self.ms_per_frame / 1000.0
        self.opacity_effect: QGraphicsOpacityEffect = QGraphicsOpacityEffect()
        self.text_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(self.MAX_OPACITY)
        self.start_in_center()
        logging.debug("PowAnimation initialized.")

    def animate(self) -> None:
        """
        Handle the animation phases: fade-in, display, and fade-out.
        Applies jiggle effect if enabled.
        Stops the animation after completion.
        """

        try:
            self.elapsed_time += self.delta_time
            if self.elapsed_time <= self.fade_in_time:
                self._handle_fade_in()
            elif self.elapsed_time <= self.fade_in_time + self.display_time:
                self._handle_display()
            elif self.elapsed_time <= self.duration:
                self._handle_fade_out()

            if self._should_jiggle():
                self._apply_jiggle()

            if self.elapsed_time >= self.duration:
                logging.debug("Animation duration reached. Stopping animation.")
                self.stop()
        except Exception as e:
            logging.exception("An error occurred during animation: %s", e)
            self.stop()

    def stop(self) -> None:
        """
        Stop the animation and delete the text label.
        """
        super().stop()
        try:
            self.text_label.deleteLater()
            logging.debug("PowAnimation stopped and label deleted.")
        except Exception as e:
            logging.exception("Failed to delete text label: %s", e)

    def handle_collision(self, percentage=0.10):
        """
        Manually increase the elapsed time to bump the animation ahead based on a percentage of its duration.

        Args:
            percentage (float): The percentage of the animation's duration to bump.
        """
        bump_x = self.text_label.x()
        bump_y = self.text_label.y()
        bump_y += 18
        self.text_label.move(bump_x, bump_y)

    def _handle_fade_in(self) -> None:
        """
        Handle the fade-in phase by scaling the text.
        """
        scale_progress: float = self.elapsed_time / self.fade_in_time
        new_height: float = self.font_size * (1.0 + (self.text_delta * (1.0 - scale_progress)))
        new_font_size: int = max(self.MIN_FONT_SIZE, int(new_height))
        self.text_label.setFont(QFont(self.text_label.font().family(), new_font_size))
        self.text_label.adjustSize()
        self._recenter_text()

    def _handle_display(self) -> None:
        """
        Handle the display phase by ensuring the text is properly sized and centered.
        """
        self.text_label.adjustSize()
        self._recenter_text()

    def _handle_fade_out(self) -> None:
        """
        Handle the fade-out phase by adjusting text opacity.
        """
        fade_progress: float = (
                                       self.elapsed_time - self.fade_in_time - self.display_time
                               ) / self.fade_out_time
        opacity: float = max(0.0, 1.0 - fade_progress)
        self.opacity_effect.setOpacity(opacity)

    def _should_jiggle(self) -> bool:
        """
        Determine if the jiggle effect should be applied.

        Returns:
            bool: True if jiggle effect should be applied, False otherwise.
        """
        return (
                self.behavior == "Jiggle"
                and self.elapsed_time > self.fade_in_time
                and (self.elapsed_time - self.jiggle_last_time) > self.jiggle_delay_time
        )

    def _apply_jiggle(self) -> None:
        """
        Apply the jiggle effect by randomly adjusting the label's position.
        """
        try:
            new_x: int = self.text_label.x() + random.randint(-self.JIGGLE_RANGE, self.JIGGLE_RANGE)
            new_y: int = self.text_label.y() + random.randint(-self.JIGGLE_RANGE, self.JIGGLE_RANGE)
            self.text_label.move(new_x, new_y)
            self.jiggle_last_time = self.elapsed_time
        except Exception as e:
            logging.exception("Failed to apply jiggle effect: %s", e)

    def _recenter_text(self) -> None:
        """
        Recenter the text label after adjusting its size.
        """
        try:
            parent_width: int = self.text_label.parentWidget().width()
            label_width: int = self.text_label.width()
            new_x: int = (parent_width - label_width) // 2
            self.text_label.move(new_x, self.text_label.y())
        except Exception as e:
            logging.exception("Failed to recenter text: %s", e)
