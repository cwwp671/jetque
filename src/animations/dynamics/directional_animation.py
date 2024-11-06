# src/animations/dynamics/directional_animation.py

import logging

from PyQt6.QtCore import QEasingCurve, QPointF, QObject
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.dynamic_animation import DynamicAnimation
from src.animations.animation_label import AnimationLabel


class DirectionalAnimation(DynamicAnimation):
    """
    Handles directional animations, moving the label from the starting position
    to the ending position based on the specified direction. There is no difference between this and its parent,
    however it exists to keep track of the subtype
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
        Initialize the DirectionalAnimation with the given parameters.

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
        # Currently no unique DirectionalAnimation init logic
        logging.debug("DirectionalAnimation initialized.")
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
            label=label,
            ending_position=ending_position,
            easing_style=easing_style
        )

    def play(self) -> None:
        """
        Play the directional animation.
        """
        try:
            # Currently no unique DirectionalAnimation play logic
            logging.info("DirectionalAnimation played.")
            super().play()
        except Exception as e:
            logging.exception("Failed to play DirectionalAnimation: %s", e)

    def stop(self) -> None:
        """
        Stop the directional animation.
        """
        try:
            # Currently no unique DirectionalAnimation stop logic
            logging.info("DirectionalAnimation stopped.")
            super().stop()
        except Exception as e:
            logging.exception("Failed to stop DirectionalAnimation: %s", e)

    def _setup_animations(self) -> None:
        """
        Set up the directional animation settings and groups.
        """
        try:
            # Currently no unique DirectionalAnimation setup logic
            logging.debug("DirectionalAnimation animations set up.")
            super()._setup_animations()
        except Exception as e:
            logging.exception("Failed to set up DirectionalAnimation animations: %s", e)

    def _connect_signals(self) -> None:
        """
        Connect directional animation signals to handlers.
        """
        try:
            # Currently no unique DirectionalAnimation setup logic
            logging.debug("DirectionalAnimation signals connected.")
            super()._connect_signals()
        except Exception as e:
            logging.exception("Failed to connect DirectionalAnimation signals: %s", e)
