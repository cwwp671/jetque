import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from PyQt6.QtCore import QObject, QEasingCurve, pyqtSignal, QUrl
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation_label import AnimationLabel

# Constants
DEFAULT_SOUND_VOLUME: float = 0.5  # Volume range: 0.0 to 1.0


class Animation(QObject, ABC):
    """
    Abstract base class for all animations.

    Attributes:
        finished (pyqtSignal): Signal emitted when the animation finishes.
    """

    finished = pyqtSignal()

    def __init__(
            self,
            parent: QObject,
            animation_type: str,
            sound: Optional[str],
            icon: Any,
            text: str,
            duration: float,
            starting_position: Any,
            fade_in: bool,
            fade_out: bool,
            fade_in_percentage: float,
            fade_out_percentage: float,
            fade_in_easing_style: QEasingCurve.Type,
            fade_out_easing_style: QEasingCurve.Type,
            label: AnimationLabel
    ) -> None:
        """
        Initialize the Animation with the given parameters.

        Args:
            parent (QObject): The parent QObject.
            animation_type (str): Type/style of the animation.
            sound (Optional[str]): Path to the sound file to play.
            icon (Any): Icon of the animation.
            text (str): Message string of the animation.
            duration (float): Duration of the animation in seconds.
            starting_position (Any): Starting position of the animation.
            fade_in (bool): Whether to apply fade-in effect.
            fade_out (bool): Whether to apply fade-out effect.
            fade_in_percentage (float): Percentage of duration for fade-in.
            fade_out_percentage (float): Percentage of duration for fade-out.
            fade_in_easing_style (QEasingCurve.Type): Easing curve for fade-in.
            fade_out_easing_style (QEasingCurve.Type): Easing curve for fade-out.
            label (AnimationLabel): The label associated with the animation.
        """
        super().__init__(parent)
        self.type: str = animation_type
        self.sound: Optional[str] = sound
        self.label: AnimationLabel = label
        self.duration: float = duration
        self.starting_position: Any = starting_position
        self.fade_in: bool = fade_in
        self.fade_in_percentage: float = fade_in_percentage
        self.fade_in_easing_style: QEasingCurve.Type = fade_in_easing_style
        self.fade_out: bool = fade_out
        self.fade_out_percentage: float = fade_out_percentage
        self.fade_out_easing_style: QEasingCurve.Type = fade_out_easing_style
        self.sound_effect: Optional[QSoundEffect] = None

        self.setup_animations()
        self._connect_signals()
        self._initialize_sound()
        logging.debug("Animation initialized: Type=%s", self.type)

    @abstractmethod
    def play(self) -> None:
        """
        Start the animation.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the animation.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def setup_animations(self) -> None:
        """
        Set up the animations.
        Must be implemented by subclasses.
        """
        pass

    def _connect_signals(self) -> None:
        """
        Connect necessary signals to handlers.
        """
        try:
            self.label.showEvent = self._on_show
            logging.debug("Signals connected for Animation")
        except Exception as e:
            logging.exception("Failed to connect signals: %s", e)

    def _initialize_sound(self) -> None:
        """
        Initialize the sound effect if a sound file is provided.
        """
        if not self.sound:
            logging.debug("No sound file provided for Animation.")
            return

        try:
            self.sound_effect = QSoundEffect()
            self.sound_effect.setSource(QUrl.fromLocalFile(self.sound))
            self.sound_effect.setVolume(DEFAULT_SOUND_VOLUME)
            logging.debug("Sound initialized for Animation: %s", self.sound)
        except Exception as e:
            logging.exception("Error initializing sound for Animation: %s", e)

    def play_sound(self) -> None:
        """
        Play the associated sound effect if available.
        """
        if not self.sound_effect:
            logging.debug("No sound effect to play for Animation.")
            return

        try:
            self.sound_effect.play()
            logging.debug("Sound played for Animation.")
        except Exception as e:
            logging.exception("Error playing sound for Animation: %s", e)

    def _on_show(self, event: Any) -> None:
        """
        Handle the show event of the label.

        Args:
            event (Any): The show event.
        """
        try:
            self.play_sound()
            event.accept()
            logging.debug("Handled show event for Animation.")
        except Exception as e:
            logging.exception("Error handling show event: %s", e)
