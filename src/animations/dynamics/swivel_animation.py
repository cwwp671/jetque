# src/animations/dynamics/swivel_animation.py

import logging
from typing import Tuple

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QObject, QSequentialAnimationGroup
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.dynamic_animation import DynamicAnimation
from src.animations.animation_label import AnimationLabel


class SwivelAnimation(DynamicAnimation):
    """
    Handles swivel animations, moving the label in two phases:
    phase 1 to the swivel position and phase 2 to the ending position.
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
            phase_1_duration: int,
            phase_2_duration: int,
            swivel_position: QPointF
    ) -> None:
        """
        Initialize the SwivelAnimation with the given parameters.

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
            phase_1_duration (int): The duration of phase 1
            phase_2_duration (int): The duration of phase 2
            swivel_position (QPointF): The Swivel position for the animation.
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
        self.phase_1_duration: int = phase_1_duration
        self.phase_2_duration: int = phase_2_duration
        self.swivel_position: QPointF = swivel_position
        self.animation_group: QSequentialAnimationGroup = QSequentialAnimationGroup()
        logging.debug("SwivelAnimation initialized.")

    def play(self) -> None:
        """
        Start the swivel animation.
        """
        try:
            self.play_sound()
            self.animation_group.start()
            logging.info("SwivelAnimation started.")
        except Exception as e:
            logging.exception("Failed to play SwivelAnimation: %s", e)

    def stop(self) -> None:
        """
        Stop the swivel animation.
        """
        try:
            self.animation_group.stop()
            logging.info("SwivelAnimation stopped.")
        except Exception as e:
            logging.exception("Failed to stop SwivelAnimation: %s", e)

    def setup_animations(self) -> None:
        """
        Set up the swivel animation settings and groups.
        """
        try:
            # Phase 1 Animation
            phase_1_animation = QPropertyAnimation(self.label, b"pos")
            phase_1_animation.setDuration(self.phase_1_duration)
            phase_1_animation.setStartValue(self.starting_position)
            phase_1_animation.setEndValue(self.swivel_position)
            phase_1_animation.setEasingCurve(self.easing_style)
            logging.debug("Phase 1 animation set up with duration %d ms.", self.phase_1_duration)

            # Phase 2 Animation
            phase_2_animation = QPropertyAnimation(self.label, b"pos")
            phase_2_animation.setDuration(self.phase_2_duration)
            phase_2_animation.setStartValue(self.swivel_position)
            phase_2_animation.setEndValue(self.ending_position)
            phase_2_animation.setEasingCurve(self.easing_style)
            logging.debug("Phase 2 animation set up with duration %d ms.", self.phase_2_duration)

            # Add animations to the group
            self.animation_group.addAnimation(phase_1_animation)
            self.animation_group.addAnimation(phase_2_animation)
            self.animation_group.finished.connect(self.finished.emit)
            logging.debug("SwivelAnimation animations set up.")
        except Exception as e:
            logging.exception("Failed to set up SwivelAnimation animations: %s", e)

    def _connect_signals(self) -> None:
        """
        Connect swivel animation signals to handlers.
        """
        try:
            super()._connect_signals()
            # Additional signal connections can be added here if needed
            logging.debug("SwivelAnimation signals connected.")
        except Exception as e:
            logging.exception("Failed to connect SwivelAnimation signals: %s", e)

    def _connect_slots(self) -> None:
        """
        Connect swivel animation slots to handlers.
        """
        try:
            super()._connect_slots()
            # Additional slot connections can be added here if needed
            logging.debug("SwivelAnimation slots connected.")
        except Exception as e:
            logging.exception("Failed to connect SwivelAnimation slots: %s", e)
