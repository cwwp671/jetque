# src/animations/dynamic_animation.py

import logging

from PyQt6.QtCore import QObject, QEasingCurve, QPointF
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation import Animation
from src.animations.animation_label import AnimationLabel


class DynamicAnimation(Animation):
    """
    Base class for dynamic animations, handling common functionalities for dynamic animations.

    Attributes:
        ending_position (QPointF): The ending position of the animation.
        easing_style (QEasingCurve.Type): The easing curve type for the animation.
    """

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
            label: AnimationLabel,
            ending_position: QPointF,
            easing_style: QEasingCurve.Type
    ) -> None:
        """
        Initialize the DynamicAnimation with the given parameters.

        Args:
            parent (QObject): The parent object.
            animation_type (str): The type of animation.
            sound (QSoundEffect): The sound effect to play.
            duration (int): The duration of the animation in milliseconds.
            starting_position (QPointF): The starting position of the animation.
            fade_in (bool): Whether the animation fades in.
            fade_out (bool): Whether the animation fades out.
            fade_in_duration (int): The duration for fade-in in milliseconds.
            fade_out_duration (int): The duration for fade-out in milliseconds.
            fade_out_delay (int): The fade-out delay in milliseconds.
            fade_in_easing_style (QEasingCurve.Type): The easing curve for fade-in.
            fade_out_easing_style (QEasingCurve.Type): The easing curve for fade-out.
            label (AnimationLabel): The label associated with the animation.
            ending_position (QPointF): The ending position of the animation.
            easing_style (QEasingCurve.Type): The easing curve type for the animation.
        """
        self.ending_position: QPointF = ending_position
        self.easing_style: QEasingCurve.Type = easing_style
        logging.debug("DynamicAnimation initialized.")
        super().__init__(
            parent=parent,
            animation_type=animation_type,
            sound=sound,
            duration=duration,
            starting_position=starting_position,
            fade_in=fade_in,
            fade_out=fade_out,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration,
            fade_out_delay=fade_out_delay,
            fade_in_easing_style=fade_in_easing_style,
            fade_out_easing_style=fade_out_easing_style,
            label=label
        )

    def play(self) -> None:
        """
        Play the dynamic animation.
        """
        try:
            # Currently no unique DynamicAnimation play logic
            logging.info("DynamicAnimation played.")
            super().play()
        except Exception as e:
            logging.exception("Failed to play DynamicAnimation: %s", e)

    def stop(self) -> None:
        """
        Stop the dynamic animation.
        """
        try:
            # Currently no unique DynamicAnimation stop logic
            logging.info("DynamicAnimation stopped.")
            super().stop()
        except Exception as e:
            logging.exception("Failed to stop DynamicAnimation: %s", e)

    def _setup_animations(self) -> None:
        """
        Set up the dynamic animation settings and groups.
        """
        logging.debug("Setting up DynamicAnimation animations.")
        try:
            self.animation.setEndValue(self.ending_position)
            self.animation.setEasingCurve(self.easing_style)
            logging.debug("DynamicAnimation animations set up.")
            super()._setup_animations()
        except Exception as e:
            logging.exception("Error setting up DynamicAnimation: %s", e)

    def _connect_signals(self) -> None:
        """
        Connect any necessary dynamic animation signals to handlers.
        """
        try:
            # Currently no unique dynamic signal logic
            logging.debug("Signals connected for DynamicAnimation")
            super()._connect_signals()
        except Exception as e:
            logging.exception("Failed to connect DynamicAnimation signals: %s", e)
