# src/animations/animation.py

import logging

from PyQt6.QtCore import (
    QObject, QEasingCurve, pyqtSignal, QPointF, QParallelAnimationGroup, QPropertyAnimation, QSequentialAnimationGroup
)
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation_label import AnimationLabel


class Animation(QObject):
    """
    Base class for all animations.

    Attributes:
        finished (pyqtSignal): Signal emitted when the animation finishes.
    """

    finished: pyqtSignal = pyqtSignal()

    def __init__(
            self,
            parent: QObject,
            animation_type: str,
            sound: QSoundEffect,
            duration: int,
            starting_position: QPointF,
            fade_in: bool,
            fade_out: bool,
            fade_in_duration: int,
            fade_out_duration: int,
            fade_out_delay: int,
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
            fade_in_duration (int): The duration for fade-in in milliseconds.
            fade_out_duration (int): The duration for fade-out in milliseconds.
            fade_out_delay (int): The fade-out delay in milliseconds.
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
        self.fade_in_duration: int = fade_in_duration
        self.fade_in_easing_style: QEasingCurve.Type = fade_in_easing_style
        self.fade_out: bool = fade_out
        self.fade_out_duration: int = fade_out_duration
        self.fade_out_delay: int = fade_out_delay
        self.fade_out_easing_style: QEasingCurve.Type = fade_out_easing_style
        self.animation_group: QParallelAnimationGroup = QParallelAnimationGroup()
        self.animation: QPropertyAnimation = QPropertyAnimation(self.label, b"pos")

        if self.fade_in:
            self.fade_in_animation: QPropertyAnimation = QPropertyAnimation(self.label, b"opacity")

        if self.fade_out:
            self.fade_out_animation: QPropertyAnimation = QPropertyAnimation(self.label, b"opacity")
            self.fade_out_group: QSequentialAnimationGroup = QSequentialAnimationGroup()

        self._setup_animations()
        self._connect_signals()
        logging.debug("Animation initialized: Type=%s", self.type)

    def play(self) -> None:
        """
        Play the animation.
        """
        try:
            self._play_sound()
            self.label.show()
            self.animation_group.start()
            logging.debug("Animation played.")
        except Exception as e:
            logging.exception("Failed to play Animation: %s", e)

    def stop(self) -> None:
        """
        Stop the animation.
        """
        try:
            self.animation_group.stop()
            logging.debug("Animation stopped.")
        except Exception as e:
            logging.exception("Failed to stop Animation: %s", e)

    def _setup_animations(self) -> None:
        """
        Set up the animation settings and groups.
        """
        logging.debug("Setting up Animation.")
        try:
            if self.fade_in:
                self.fade_in_animation.setDuration(self.fade_in_duration)
                self.fade_in_animation.setStartValue(0.0)
                self.fade_in_animation.setEndValue(1.0)
                self.fade_in_animation.setEasingCurve(self.fade_in_easing_style)
                self.animation_group.addAnimation(self.fade_in_animation)

            if self.fade_out:
                self.fade_out_animation.setDuration(self.fade_out_duration)
                self.fade_out_animation.setStartValue(1.0)
                self.fade_out_animation.setEndValue(0.0)
                self.fade_out_animation.setEasingCurve(self.fade_out_easing_style)
                self.fade_out_group.addPause(self.fade_out_delay)  # Sequential group: first pause, then fade out
                self.fade_out_group.addAnimation(self.fade_out_animation)
                self.animation_group.addAnimation(self.fade_out_group)

            self.animation.setDuration(self.duration)
            self.animation.setStartValue(self.starting_position)
            self.animation_group.addAnimation(self.animation)
            logging.debug("Animation set up.")
        except Exception as e:
            logging.exception("Error setting up Animation: %s", e)

    def _play_sound(self) -> None:
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
            self.animation_group.finished.connect(self.finished.emit)
            logging.debug("Signals connected for Animation")
        except Exception as e:
            logging.exception("Failed to connect Animation signals: %s", e)
