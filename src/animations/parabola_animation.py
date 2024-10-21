import logging

from PyQt6.QtWidgets import QGraphicsOpacityEffect
from src.animations.animation import Animation


class ParabolaAnimation(Animation):
    """Implements a parabolic animation with a fade-out effect for a text label.

    The label moves along a parabolic path and fades out based on the provided
    configuration.
    """

    DEFAULT_DURATION: float = 1.5
    MIN_OPACITY: float = 0.0
    MAX_OPACITY: float = 1.0

    def __init__(self, text_label, config: dict) -> None:
        """Initialize the ParabolaAnimation with label and configuration.

        Args:
            text_label: The label to animate.
            config: Configuration dictionary for the animation behavior.
        """
        super().__init__(text_label, config)
        self.duration: float = self.DEFAULT_DURATION
        self.parent_widget = text_label.parentWidget()
        self.scroll_width: float = self.parent_widget.width()
        self.scroll_height: float = self.parent_widget.height()

        # Set initial positions and parameters for the parabola
        self.start_x: float = 0.0
        self.start_y: float = 0.0
        self.vertex_x: float = 0.0
        self.vertex_y: float = 0.0
        self.end_x: float = 0.0
        self.end_y: float = 0.0
        self.curvature_factor: float = 0.0

        # Extract configuration
        animation_config: dict = config['text']['animation']
        self.behavior: str = animation_config.get('behavior')
        self.direction: str = animation_config.get('direction')

        logging.debug(f"Animation Behavior: {self.behavior}, Animation Direction: {self.direction}")

        # Get label dimensions
        self.label_width: float = self.text_label.width()
        self.label_height: float = self.text_label.height()

        logging.debug(f"Label Width: {self.label_width}, Label Height: {self.label_height}")

        # Calculate initial parabola parameters
        self._calculate_parabola_parameters()

        # Timing setup
        self.ms_per_frame: int = self.config['text']['animation']['ms_per_frame']
        self.delta_time: float = self.ms_per_frame / 1000.0

        # Initialize opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.text_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(self.MAX_OPACITY)

        # Set the initial position and display the label
        self.text_label.set_position(self.start_x, self.start_y)
        self.text_label.show()

    def animate(self) -> None:
        """Perform the animation and calculate parabolic trajectory."""
        self.elapsed_time += self.delta_time
        progress: float = min(1.0, self.elapsed_time / self.duration)

        # Calculate X position based on behavior
        x_position: float = self._calculate_x_position(progress)

        # Calculate Y position based on the parabolic equation
        y_position: float = self.curvature_factor * (x_position - self.vertex_x) ** 2.0 + self.vertex_y

        # Set the label's new position
        self.text_label.set_position(x_position, y_position)

        # Update opacity for fade-out effect
        opacity: float = self._calculate_opacity(x_position)
        self.opacity_effect.setOpacity(opacity)

        # Stop the animation once it's complete
        if self.elapsed_time >= self.duration:
            self.stop()

    def stop(self) -> None:
        """Stop the animation and delete the text label."""
        super().stop()
        self.text_label.deleteLater()
        logging.debug("ParabolaAnimation stopped and label deleted.")

    def _calculate_parabola_parameters(self) -> None:
        """Calculate the parameters for the parabola based on behavior and direction."""
        # Set common Y values and vertex X
        self.start_y = (self.scroll_height / 2.0) - (self.label_height / 2.0)
        self.vertex_x = (self.scroll_width / 2.0) - (self.label_width / 2.0)
        self.end_y = self.start_y

        if self.behavior == 'CurvedLeft':
            self.start_x = self.scroll_width - self.label_width
            self.end_x = 0.0
        else:  # CurvedRight
            self.start_x = 0.0
            self.end_x = self.scroll_width - self.label_width

        if self.direction == 'Up':
            self.vertex_y = self.label_height
        else:  # Down
            self.vertex_y = self.scroll_height - self.label_height

        # Calculate curvature based on vertex and start/end points
        self.curvature_factor = self._calculate_curvature(self.start_x, self.start_y, self.vertex_x, self.vertex_y)

        logging.debug(f"Parabola parameters calculated: start=({self.start_x}, {self.start_y}), "
                      f"vertex=({self.vertex_x}, {self.vertex_y}), end=({self.end_x}, {self.end_y}), "
                      f"curvature={self.curvature_factor}")

    def _calculate_x_position(self, progress: float) -> float:
        """Calculate the X position based on animation progress and behavior."""
        if self.behavior == 'CurvedLeft':
            return self.start_x - (self.start_x - self.end_x) * progress
        return self.start_x + (self.end_x - self.start_x) * progress

    def _calculate_opacity(self, x_position: float) -> float:
        """Calculate the opacity based on the position to create a fade-out effect."""
        try:
            if self.behavior == 'CurvedLeft' and x_position <= self.vertex_x:
                distance_from_peak: float = abs(x_position - self.vertex_x)
                total_horizontal_distance: float = abs(self.end_x - self.vertex_x)
                opacity: float = max(
                    self.MIN_OPACITY,
                    self.MAX_OPACITY - (distance_from_peak / total_horizontal_distance)
                )
            elif self.behavior == 'CurvedRight' and x_position >= self.vertex_x:
                distance_from_peak: float = abs(x_position - self.vertex_x)
                total_horizontal_distance: float = abs(self.end_x - self.vertex_x)
                opacity: float = max(
                    self.MIN_OPACITY,
                    self.MAX_OPACITY - (distance_from_peak / total_horizontal_distance)
                )
            else:
                opacity = self.MAX_OPACITY

            return opacity
        except Exception as e:
            logging.error(f"Exception in calculate_opacity(): {e}")
            return self.MAX_OPACITY  # Default to fully opaque in case of error

    @staticmethod
    def _calculate_curvature(start_x: float, start_y: float, vertex_x: float, vertex_y: float) -> float:
        """Calculate the curvature factor based on parabola's start and vertex points."""
        return (start_y - vertex_y) / ((start_x - vertex_x) ** 2.0)
