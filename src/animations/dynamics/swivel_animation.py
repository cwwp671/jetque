# src/animations/dynamics/swivel_animation.py

import logging

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QObject
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
            fade_in_duration: int,
            fade_out_duration: int,
            fade_out_delay: int,
            fade_in_easing_style: QEasingCurve.Type,
            fade_out_easing_style: QEasingCurve.Type,
            label: AnimationLabel,
            ending_position: QPointF,
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
            fade_in_duration (int): The duration for fade-in in milliseconds.
            fade_out_duration (int): The duration for fade-out in milliseconds.
            fade_out_delay (int): The fade-out delay in milliseconds.
            fade_in_easing_style (QEasingCurve.Type): The easing curve for fade-in.
            fade_out_easing_style (QEasingCurve.Type): The easing curve for fade-out.
            label (AnimationLabel): The label associated with the animation.
            ending_position (QPointF): The ending position of the animation.
            easing_style (QEasingCurve.Type): The easing curve type for the animation.
            phase_1_duration (int): The duration of phase 1
            phase_2_duration (int): The duration of phase 2
            swivel_position (QPointF): The Swivel position for the animation.
        """
        self.phase_1_duration: int = phase_1_duration
        self.phase_2_duration: int = phase_2_duration
        self.swivel_position: QPointF = swivel_position
        self.animation2 = QPropertyAnimation(self.label, b"pos")
        logging.debug("SwivelAnimation initialized.")
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

    def setup_animations(self) -> None:
        """
        Set up the swivel animation settings and groups.
        """
        try:
            super()._setup_animations()
            self.animation.setDuration(self.phase_1_duration)
            self.animation.setEndValue(self.swivel_position)
            logging.debug("Phase 1 animation set up with duration %d ms.", self.phase_1_duration)
            self.animation2.setDuration(self.phase_2_duration)
            self.animation2.setStartValue(self.swivel_position)
            self.animation2.setEndValue(self.ending_position)
            self.animation2.setEasingCurve(self.easing_style)
            logging.debug("Phase 2 animation set up with duration %d ms.", self.phase_2_duration)
            self.animation_group.addAnimation(self.animation2)
            logging.debug("SwivelAnimation animations set up.")
        except Exception as e:
            logging.exception("Failed to set up SwivelAnimation animations: %s", e)
