# animation/pow_animation.py
import logging
import random

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from src.animations.animation import Animation


class PowAnimation(Animation):
    """Implements Pow animation with scaling, display, and fade out."""

    FADE_IN_TIME = 0.17
    DISPLAY_TIME = 1.5
    FADE_OUT_TIME = 0.5
    TEXT_DELTA = 0.7
    JIGGLE_DELAY_TIME = 0.05

    def __init__(self, text_label, config):
        super().__init__(text_label, config)
        self.fade_in_time = self.FADE_IN_TIME
        self.display_time = self.DISPLAY_TIME
        self.fade_out_time = self.FADE_OUT_TIME
        self.text_delta = self.TEXT_DELTA
        self.jiggle_delay_time = self.JIGGLE_DELAY_TIME
        self.jiggle_last_time = 0
        self.font_size = text_label.font().pointSize()
        self.duration = self.fade_in_time + self.display_time + self.fade_out_time
        self.behavior = config['text']['animation'].get('behavior', 'Normal')
        self.ms_per_frame = self.config['text']['animation']['ms_per_frame']
        self.delta_time = self.ms_per_frame / 1000.0
        self.opacity_effect = QGraphicsOpacityEffect()
        self.text_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        logging.debug("PowAnimation initialized.")

    def animate(self):
        """Handle the animation phases."""
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

    def _handle_fade_in(self):
        """Handle the fade-in phase by scaling the text."""
        scale_progress = self.elapsed_time / self.fade_in_time
        new_height = self.font_size * (1 + (self.text_delta * (1 - scale_progress)))
        new_font_size = max(1, int(new_height))
        self.text_label.setFont(QFont(self.text_label.font().family(), new_font_size))
        self.text_label.adjustSize()
        self._recenter_text()

    def _handle_display(self):
        """Handle the display phase."""
        self.text_label.adjustSize()
        self._recenter_text()

    def _handle_fade_out(self):
        """Handle the fade-out phase by adjusting text opacity."""
        fade_progress = (
                            self.elapsed_time - self.fade_in_time - self.display_time
                        ) / self.fade_out_time
        opacity = max(0, 1 - fade_progress)
        self.opacity_effect.setOpacity(opacity)

    def _should_jiggle(self):
        """Determine if the jiggle effect should be applied."""
        return (
                self.behavior == "Jiggle"
                and self.elapsed_time > self.fade_in_time
                and self.elapsed_time - self.jiggle_last_time > self.jiggle_delay_time
        )

    def _apply_jiggle(self):
        """Apply the jiggle effect by randomly adjusting the label's position."""
        new_x = self.text_label.x() + random.randint(-1, 1)
        new_y = self.text_label.y() + random.randint(-1, 1)
        self.text_label.move(new_x, new_y)
        self.jiggle_last_time = self.elapsed_time

    def _recenter_text(self):
        """Recenter the text label after adjusting its size."""
        parent_width = self.text_label.parentWidget().width()
        label_width = self.text_label.width()
        new_x = (parent_width - label_width) // 2
        self.text_label.move(new_x, self.text_label.y())

    def stop(self):
        """Stop the animation and delete the text label."""
        super().stop()
        self.text_label.deleteLater()
        logging.debug("PowAnimation stopped and label deleted.")
