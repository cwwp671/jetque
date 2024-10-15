# animation/parabola_animation.py
import logging

from PyQt6.QtWidgets import QGraphicsOpacityEffect
from src.animations.animation import Animation


class ParabolaAnimation(Animation):
    """Implements parabola animation with fade-out effect."""

    DEFAULT_DURATION = 1.5

    def __init__(self, text_label, config):
        super().__init__(text_label, config)
        self.duration = self.DEFAULT_DURATION
        self.parent_widget = text_label.parentWidget()
        self.scroll_width = self.parent_widget.width()
        self.scroll_height = self.parent_widget.height()

        animation_config = config['text']['animation']
        self.behavior = animation_config.get('behavior', 'CurvedLeft')
        self.direction = animation_config.get('direction', 'Up')

        self.start_x = self.scroll_width / 2
        self.start_y = self.scroll_height / 2

        self.end_x = 0 if self.behavior == 'CurvedLeft' else self.scroll_width
        self.h, self.k, self.a = self._calculate_parabola_parameters()

        self.ms_per_frame = self.config['text']['animation']['ms_per_frame']
        self.delta_time = self.ms_per_frame / 1000.0

        # Initialize opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.text_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

        logging.debug(
            f"ParabolaAnimation initialized with behavior: {self.behavior}, "
            f"direction: {self.direction}, vertex: ({self.h}, {self.k}), a: {self.a}"
        )

    def _calculate_parabola_parameters(self):
        """Calculate the parameters for the parabola based on behavior and direction."""
        if self.behavior == 'CurvedLeft':
            h = self.scroll_width / 4
        else:  # 'CurvedRight'
            h = 3 * self.scroll_width / 4

        if self.direction == 'Up':
            a = 4 * self.scroll_height / self.scroll_width ** 2
            k = self.start_y / 2
        else:  # 'Down'
            a = -4 * self.scroll_height / self.scroll_width ** 2
            k = self.start_y + (self.scroll_height / 4)

        logging.debug(f"Parabola parameters calculated: h={h}, k={k}, a={a}")
        return h, k, a

    def animate(self):
        """Perform the animation and calculate parabolic trajectory."""
        self.elapsed_time += self.delta_time
        progress = min(1, self.elapsed_time / self.duration)

        x_position = self.start_x + (self.end_x - self.start_x) * progress
        y_position = self.a * (x_position - self.h) ** 2 + self.k

        self.text_label.set_position_centered(x_position, y_position)

        opacity = self._calculate_opacity(x_position)
        self.opacity_effect.setOpacity(opacity)

        if self.elapsed_time >= self.duration:
            logging.debug("Animation duration reached. Stopping animation.")
            self.stop()

    def _calculate_opacity(self, x_position):
        """Calculate the opacity based on the position to create a fade-out effect."""
        try:
            if self.behavior == 'CurvedLeft':
                if x_position <= self.h:
                    distance_from_peak = abs(x_position - self.h)
                    total_horizontal_distance = abs(self.end_x - self.h)
                    opacity = max(0, 1 - (distance_from_peak / total_horizontal_distance))
                else:
                    opacity = 1
            elif self.behavior == 'CurvedRight':
                if x_position >= self.h:
                    distance_from_peak = abs(x_position - self.h)
                    total_horizontal_distance = abs(self.end_x - self.h)
                    opacity = max(0, 1 - (distance_from_peak / total_horizontal_distance))
                else:
                    opacity = 1
            else:
                opacity = 1
            return opacity
        except Exception as e:
            logging.error(f"Exception in calculate_opacity(): {e}")
            return 1.0  # Default to fully opaque in case of error

    def stop(self):
        """Stop the animation and delete the text label."""
        super().stop()
        self.text_label.deleteLater()
        logging.debug("ParabolaAnimation stopped and label deleted.")
