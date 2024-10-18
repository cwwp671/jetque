# jetque/src/animations/angled_animation.py

import logging
from src.animations.animation import Animation
from PyQt6.QtWidgets import QGraphicsOpacityEffect

class AngledAnimation(Animation):
    """Implements Angled animation (AngleUp/AngleDown and Left/Right)."""

    ANGLED_WIDTH_PERCENT = 0.95
    ANGLED_HEIGHT_PERCENT = 0.95
    HORIZONTAL_PHASE_PERCENT = 0.5

    def __init__(self, text_label, config):
        super().__init__(text_label, config)
        animation_config = config['text']['animation']
        self.direction = animation_config.get('direction', 'Left')
        self.behavior = animation_config.get('behavior', 'AngleUp')

        self.start_x = text_label.x()
        self.start_y = text_label.y()
        self.finish_x = self.start_x
        self.finish_y = self.start_y

        self.angle_finish_x = None
        self.angle_finish_y = None

        self._calculate_finish_position()
        logging.debug(
            f"AngledAnimation initialized with direction: {self.direction}, "
            f"behavior: {self.behavior}"
        )

        self.ms_per_frame = self.config['text']['animation']['ms_per_frame']
        self.delta_time = self.ms_per_frame / 1000.0
        logging.debug(
            f"AngledAnimation initialized with ms_per_frame: {self.ms_per_frame} ms, "
            f"delta_time: {self.delta_time} seconds."
        )

        self.opacity_effect = QGraphicsOpacityEffect()
        self.text_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

    def _calculate_finish_position(self):
        """Calculate finish positions based on direction and behavior, considering label width."""
        parent_widget = self.text_label.parentWidget()
        parent_width = parent_widget.width()
        parent_height = parent_widget.height()
        label_width = self.text_label.width()
        label_height = self.text_label.height()

        distance_x = parent_width * self.ANGLED_WIDTH_PERCENT
        distance_y = parent_height * self.ANGLED_HEIGHT_PERCENT

        if self.direction == "Left":
            # Ensure the label's left edge doesn't go beyond the window's left boundary
            self.finish_x = max(0, self.start_x - distance_x)
        else:
            # Ensure the label's right edge doesn't go beyond the window's right boundary
            self.finish_x = min(parent_width - label_width, self.start_x + distance_x)

        if self.behavior == "AngleUp":
            # Move upwards without exceeding the window's top boundary
            self.finish_y = max(0, self.start_y - distance_y)
        else:
            # Move downwards without exceeding the window's bottom boundary
            self.finish_y = min(parent_height - label_height, self.start_y + distance_y)

        logging.debug(
            f"Calculated finish positions - X: {self.finish_x}, Y: {self.finish_y}"
        )

    def animate(self):
        """Animate text using an angled movement followed by horizontal movement."""
        try:
            self.elapsed_time += self.delta_time

            progress = self.elapsed_time / self.duration

            if progress <= self.HORIZONTAL_PHASE_PERCENT:
                # Phase 1: Angled movement
                new_x = self.start_x + (self.finish_x - self.start_x) * progress
                new_y = self.start_y + (self.finish_y - self.start_y) * progress

                self.angle_finish_x = new_x
                self.angle_finish_y = new_y
            else:
                # Phase 2: Horizontal movement
                phase_progress = (progress - self.HORIZONTAL_PHASE_PERCENT) / (
                        1 - self.HORIZONTAL_PHASE_PERCENT
                )

                parent_widget = self.text_label.parentWidget()
                parent_width = parent_widget.width()
                label_width = self.text_label.width()

                if self.direction == "Left":
                    # Move from angle_finish_x towards the left boundary (0)
                    new_x = self.angle_finish_x - (self.angle_finish_x * phase_progress)
                else:
                    # Move from angle_finish_x towards the right boundary (parent_width - label_width)
                    distance_to_boundary = (parent_width - label_width) - self.angle_finish_x
                    new_x = self.angle_finish_x + (distance_to_boundary * phase_progress)

                new_y = self.angle_finish_y
                self._handle_fade_out()

            self.text_label.move(int(new_x), int(new_y))

            if self.elapsed_time >= self.duration:
                logging.debug("Animation duration reached. Stopping animation.")
                self.stop()

        except Exception as e:
            logging.error(f"Exception in AngledAnimation.animate(): {e}")
            self.stop()

    def _handle_fade_out(self):
        """Handle the fade-out phase by adjusting text opacity."""
        fade_progress = (
                                self.elapsed_time - (self.duration * self.HORIZONTAL_PHASE_PERCENT)
                        ) / (self.duration * self.HORIZONTAL_PHASE_PERCENT)
        opacity = max(0.0, 1.0 - fade_progress)
        self.opacity_effect.setOpacity(opacity)

    def stop(self):
        """Stops the animation and deletes the text label."""
        super().stop()
        self.text_label.deleteLater()
        logging.debug("AngledAnimation stopped and label deleted.")
