# jetque/src/animations/parabola_animation.py

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
        self.start_x = 0.0
        self.start_y = 0.0
        self.vertex_x = 0.0
        self.vertex_y = 0.0
        self.end_x = 0.0
        self.end_y = 0.0
        self.curvature = 0.0
        animation_config = config['text']['animation']
        self.behavior = animation_config.get('behavior')
        self.direction = animation_config.get('direction')
        logging.debug(f"Animation Behavior: {self.behavior}, Animation Direction: {self.direction}")
        self.label_width = self.text_label.width()
        self.label_height = self.text_label.height()
        logging.debug(f"Label Width: {self.label_width}, Label Height: {self.label_height}")
        self._calculate_parabola_parameters()
        self.ms_per_frame = self.config['text']['animation']['ms_per_frame']
        self.delta_time = self.ms_per_frame / 1000.0
        self.opacity_effect = QGraphicsOpacityEffect()
        self.text_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self.text_label.set_position(self.start_x, self.start_y)
        self.text_label.show()

    def _calculate_parabola_parameters(self):
        """Calculate the parameters for the parabola based on behavior and direction."""

        # Constants
        self.start_y = (self.scroll_height / 2.0) - (self.label_height / 2.0)
        self.vertex_x = (self.scroll_width / 2.0) - (self.label_width / 2.0)
        self.end_y = self.start_y

        if self.behavior == 'CurvedLeft':
            self.start_x = self.scroll_width - self.label_width
            self.end_x = 0.0
            if self.direction == 'Up':
                self.vertex_y = self.label_height
            else:
                self.vertex_y = self.scroll_height - self.label_height
        else:
            self.start_x = 0.0
            self.end_x = self.scroll_width - self.label_width
            if self.direction == 'Up':
                self.vertex_y = self.label_height
            else:
                self.vertex_y = self.scroll_height - self.label_height

        # Calculate curvature based on vertex and start/end points
        self.curvature = (self.start_y - self.vertex_y) / ((self.start_x - self.vertex_x) ** 2.0)

        logging.debug(f"Parabola parameters calculated: start=({self.start_x}, {self.start_y}), "
                      f"vertex=({self.vertex_x}, {self.vertex_y}), end=({self.end_x}, {self.end_y}), a={self.curvature}")

    def animate(self):
        """Perform the animation and calculate parabolic trajectory."""
        self.elapsed_time += self.delta_time
        progress = min(1.0, self.elapsed_time / self.duration)

        if self.behavior == 'CurvedLeft':
            x_position = self.start_x - (self.start_x - self.end_x) * progress
        else:
            x_position = self.start_x + (self.end_x - self.start_x) * progress

        y_position = self.curvature * (x_position - self.vertex_x) ** 2.0 + self.vertex_y

        self.text_label.set_position(x_position, y_position)

        opacity = self._calculate_opacity(x_position)
        self.opacity_effect.setOpacity(opacity)

        if self.elapsed_time >= self.duration:
            self.stop()

    def _calculate_opacity(self, x_position):
        """Calculate the opacity based on the position to create a fade-out effect."""
        try:
            if self.behavior == 'CurvedLeft':
                if x_position <= self.vertex_x:
                    distance_from_peak = abs(x_position - self.vertex_x)
                    total_horizontal_distance = abs(self.end_x - self.vertex_x)
                    opacity = max(0.0, 1.0 - (distance_from_peak / total_horizontal_distance))
                else:
                    opacity = 1.0
            elif self.behavior == 'CurvedRight':
                if x_position >= self.vertex_x:
                    distance_from_peak = abs(x_position - self.vertex_x)
                    total_horizontal_distance = abs(self.end_x - self.vertex_x)
                    opacity = max(0.0, 1.0 - (distance_from_peak / total_horizontal_distance))
                else:
                    opacity = 1.0
            else:
                opacity = 1.0
            return opacity
        except Exception as e:
            logging.error(f"Exception in calculate_opacity(): {e}")
            return 1.0  # Default to fully opaque in case of error

    def stop(self):
        """Stop the animation and delete the text label."""
        super().stop()
        self.text_label.deleteLater()
        logging.debug("ParabolaAnimation stopped and label deleted.")
