# src/animations/dynamics/directional_animation.py

import logging
from typing import Tuple

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QObject
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.dynamic_animation import DynamicAnimation
from src.animations.animation_label import AnimationLabel


class DirectionalAnimation(DynamicAnimation):
    """
    Handles directional animations, moving the label from the starting position
    to the ending position based on the specified direction.
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
            fade_in_percentage: float,
            fade_out_percentage: float,
            fade_in_easing_style: QEasingCurve.Type,
            fade_out_easing_style: QEasingCurve.Type,
            label: AnimationLabel,
            ending_position: QPointF,
            direction: Tuple[float, float],
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
            fade_in_percentage (float): The percentage of duration for fade-in.
            fade_out_percentage (float): The percentage of duration for fade-out.
            fade_in_easing_style (QEasingCurve.Type): The easing curve for fade-in.
            fade_out_easing_style (QEasingCurve.Type): The easing curve for fade-out.
            label (AnimationLabel): The label associated with the animation.
            ending_position (QPointF): The ending position of the animation.
            direction (Tuple[float, float]): The direction multiplier (x, y).
            easing_style (QEasingCurve.Type): The easing curve type for the animation.
        """
        super().__init__(
            parent=parent,
            animation_type=animation_type,
            sound=sound,
            duration=duration,
            starting_position=starting_position,
            fade_in=fade_in,
            fade_out=fade_out,
            fade_in_percentage=fade_in_percentage,
            fade_out_percentage=fade_out_percentage,
            fade_in_easing_style=fade_in_easing_style,
            fade_out_easing_style=fade_out_easing_style,
            label=label,
            ending_position=ending_position,
            direction=direction,
            easing_style=easing_style
        )
        self.animation: QPropertyAnimation = QPropertyAnimation(self.label, b"pos")
        logging.debug("DirectionalAnimation initialized.")

    def play(self) -> None:
        """
        Start the directional animation.
        """
        try:
            self.play_sound()
            self.animation.start()
            logging.info("DirectionalAnimation started.")
        except Exception as e:
            logging.exception("Failed to play DirectionalAnimation: %s", e)

    def stop(self) -> None:
        """
        Stop the directional animation.
        """
        try:
            self.animation.stop()
            logging.info("DirectionalAnimation stopped.")
        except Exception as e:
            logging.exception("Failed to stop DirectionalAnimation: %s", e)

    def setup_animations(self) -> None:
        """
        Set up the directional animation settings and groups.
        """
        try:
            self.animation.setDuration(self.duration)
            self.animation.setStartValue(self.starting_position)
            self.animation.setEndValue(self.ending_position)
            self.animation.setEasingCurve(self.easing_style)
            self.animation.finished.connect(self.finished.emit)
            logging.debug("DirectionalAnimation animations set up.")
        except Exception as e:
            logging.exception("Failed to set up DirectionalAnimation animations: %s", e)

    def _connect_signals(self) -> None:
        """
        Connect directional animation signals to handlers.
        """
        try:
            super()._connect_signals()
            # Additional signal connections can be added here if needed
            logging.debug("DirectionalAnimation signals connected.")
        except Exception as e:
            logging.exception("Failed to connect DirectionalAnimation signals: %s", e)

    def _connect_slots(self) -> None:
        """
        Connect directional animation slots to handlers.
        """
        try:
            super()._connect_slots()
            # Additional slot connections can be added here if needed
            logging.debug("DirectionalAnimation slots connected.")
        except Exception as e:
            logging.exception("Failed to connect DirectionalAnimation slots: %s", e)
