# src/animations/animation.py

import logging
from abc import abstractmethod

from PyQt6.QtCore import QObject, QEasingCurve, pyqtSignal, QPointF
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation_label import AnimationLabel


class Animation(QObject):
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
            sound: QSoundEffect,
            duration: int,
            starting_position: QPointF,
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
            sound (QSoundEffect): Path to the sound file to play.
            duration (int): Duration of the animation in milliseconds.
            starting_position (QPointF): Starting position of the animation.
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
        self.sound: QSoundEffect = sound
        self.label: AnimationLabel = label
        self.duration: int = duration
        self.starting_position: QPointF = starting_position
        self.fade_in: bool = fade_in
        self.fade_in_percentage: float = fade_in_percentage
        self.fade_in_easing_style: QEasingCurve.Type = fade_in_easing_style
        self.fade_out: bool = fade_out
        self.fade_out_percentage: float = fade_out_percentage
        self.fade_out_easing_style: QEasingCurve.Type = fade_out_easing_style
        self.setup_animations()
        self._connect_signals()
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

    def play_sound(self) -> None:
        """
        Play the associated sound effect if available.
        """
        if not self.sound:
            logging.debug("No sound effect to play for Animation.")
            return

        try:
            self.sound.play()
            logging.debug("Sound played for Animation.")
        except Exception as e:
            logging.exception("Error playing sound for Animation: %s", e)

    def _connect_signals(self) -> None:
        """
        Connect necessary signals to handlers.
        """
        try:
            self.label.showEvent = self._on_show
            logging.debug("Signals connected for Animation")
        except Exception as e:
            logging.exception("Failed to connect signals: %s", e)

    def _connect_slots(self) -> None:
        """
        Connect necessary slots to handlers.
        """
        try:
            logging.debug("Slots connected for Animation")
        except Exception as e:
            logging.exception("Failed to connect slots: %s", e)

    def _on_show(self, event) -> None:
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
