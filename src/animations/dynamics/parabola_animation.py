# src/animations/dynamics/parabola_animation.py

import logging
from typing import Tuple

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QObject
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.dynamic_animation import DynamicAnimation
from src.animations.animation_label import AnimationLabel


class ParabolaAnimation(DynamicAnimation):
    """
    Handles parabolic animations, moving the label along a parabolic path
    from the starting position to the ending position based on the specified direction.
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
            easing_style: QEasingCurve.Type,
            vertex_position: QPointF
    ) -> None:
        """
        Initialize the ParabolaAnimation with the given parameters.

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
            vertex_position (QPointF): The vertex position of the animation.
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
        self.vertex_position: QPointF = vertex_position
        self.animation: QPropertyAnimation = QPropertyAnimation(self.label, b"pos")
        logging.debug("ParabolaAnimation initialized.")

    def play(self) -> None:
        """
        Start the parabolic animation.
        """
        try:
            self.play_sound()
            self.animation.start()
            logging.info("ParabolaAnimation started.")
        except Exception as e:
            logging.exception("Failed to play ParabolaAnimation: %s", e)

    def stop(self) -> None:
        """
        Stop the parabolic animation.
        """
        try:
            self.animation.stop()
            logging.info("ParabolaAnimation stopped.")
        except Exception as e:
            logging.exception("Failed to stop ParabolaAnimation: %s", e)

    def setup_animations(self) -> None:
        """
        Set up the parabolic animation settings and groups.
        """
        try:
            self.animation.setDuration(self.duration)
            self.animation.setStartValue(self.starting_position)
            self.animation.setKeyValueAt(0.5, self.vertex_position)
            self.animation.setEndValue(self.ending_position)
            self.animation.setEasingCurve(QEasingCurve.Type.Linear)
            logging.debug("ParabolaAnimation animations set up.")
        except Exception as e:
            logging.exception("Failed to set up ParabolaAnimation animations: %s", e)

    def _connect_signals(self) -> None:
        """
        Connect parabolic animation signals to handlers.
        """
        try:
            super()._connect_signals()
            self.animation.finished.connect(self.finished.emit)
            logging.debug("ParabolaAnimation signals connected.")
        except Exception as e:
            logging.exception("Failed to connect ParabolaAnimation signals: %s", e)

    def _connect_slots(self) -> None:
        """
        Connect parabolic animation slots to handlers.
        """
        try:
            super()._connect_slots()
            # Additional slot connections can be added here if needed
            logging.debug("ParabolaAnimation slots connected.")
        except Exception as e:
            logging.exception("Failed to connect ParabolaAnimation slots: %s", e)
