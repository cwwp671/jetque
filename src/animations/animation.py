# jetque/src/animations/animation.py

import logging
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class Animation(QObject):
    """Base class for all animations."""

    finished = pyqtSignal(QObject)  # Signal emitted when animation finishes

    def __init__(self, text_label, config):
        super().__init__()
        self.text_label = text_label
        self.config = config
        self.parent_widget = text_label.parentWidget()
        self.overlay_width: float = self.parent_widget.width()
        self.overlay_height: float = self.parent_widget.height()
        self.label_width: float = self.text_label.width()
        self.label_height: float = self.text_label.height()
        self.elapsed_time = 0.0
        self.start_x: float = 0.0
        self.start_y: float = 0.0
        self.duration = self.config['text']['animation'].get('duration', 1.5)
        self.animation_type = self.config['text']['animation']['type']
        self.type = self.config['text']['animation']['type']
        self._setup_timer()
        logging.debug("Animation initialized.")

    def _setup_timer(self):
        """Set up the timer for the animation."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        logging.debug("Animation timer set up and connected to animate method.")

    def play(self):
        """Start the animation."""
        self.elapsed_time = 0.0
        ms_per_frame = self.config['text']['animation'].get('ms_per_frame', 16)
        self.timer.start(ms_per_frame)
        logging.debug(f"Animation started with interval {ms_per_frame} ms.")

    def animate(self):
        """Handle the animation logic. To be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement the animate method.")

    def start_in_center(self):
        self.start_x = (self.overlay_width - self.label_width) // 2
        self.start_y = (self.overlay_height - self.label_height) // 2
        self.text_label.set_position(self.start_x, self.start_y)
        self.text_label.show()

    def stop(self):
        """Stop the animation."""
        self.timer.stop()
        self.finished.emit(self)
        logging.debug("Finished signal emitted.")

    def handle_collision(self, percentage=0.10):
        """
        Manually increase the elapsed time to bump the animation ahead based on a percentage of its duration.

        Args:
            percentage (float): The percentage of the animation's duration to bump.
        """
        delta = percentage * self.duration
        self.elapsed_time += delta
        if self.elapsed_time >= self.duration:
            logging.debug("Bumped elapsed_time exceeds duration. Stopping animation.")
            self.stop()
        else:
            logging.debug(f"New elapsed_time after bumping: {self.elapsed_time:.2f}s")
