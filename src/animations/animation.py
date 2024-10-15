# animation/animation.py
import logging

from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class Animation(QObject):
    """Base class for all animations."""

    finished = pyqtSignal(QObject)  # Signal emitted when animation finishes

    def __init__(self, text_label, config):
        super().__init__()
        self.text_label = text_label
        self.config = config
        self.elapsed_time = 0.0
        self.duration = 1.5  # Default duration
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

    def stop(self):
        """Stop the animation."""
        self.timer.stop()
        self.finished.emit(self)
        logging.debug("Finished signal emitted.")

