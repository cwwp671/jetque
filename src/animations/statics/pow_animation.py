# src/animations/statics/pow_animation.py

import logging

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.static_animation import StaticAnimation
from src.animations.OLD_animation_label import AnimationLabel


class PowAnimation(StaticAnimation):
    """
    Represents a stationary animation with no movement but may include other effects like fade in/out.
    """

    def __init__(
            self,
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
            jiggle: bool,
            jiggle_intensity: float,
            scale_percentage: float,
            scale_easing_style: QEasingCurve.Type,
            phase_1_duration: int,
            phase_2_duration: int,
            parent=None
    ) -> None:
        """
        Initialize the StationaryAnimation with the given parameters.

        Args:
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
            jiggle (bool): Whether the jiggle effect is enabled.
            jiggle_intensity (float): The intensity of the jiggle effect.
            scale_percentage (float): The amount the text scales.
            scale_easing_style (QEasingCurve.Type): The easing curve for the scaling.
            phase_1_duration: (int): The percentage of the duration to devote to phase 1.
            phase_2_duration: (int): The percentage of the duration to devote to phase 2.
            parent: The parent object.
        """
        super().__init__(
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
            jiggle=jiggle,
            jiggle_intensity=jiggle_intensity,
            parent=parent
        )

        self.scale_percentage: float = scale_percentage
        self.scale_easing_style: QEasingCurve.Type = scale_easing_style
        self.phase_1_duration: int = phase_1_duration
        self.phase_2_duration: int = phase_2_duration
        self.animation = QPropertyAnimation(self.label, b"scale")

    def _setup_animations(self) -> None:
        """
        Set up the pow animation settings and groups.
        """
        try:
            super()._setup_animations()

            if self.jiggle:
                self.jiggle_animation.addPause(self.phase_1_duration)

            self.animation.setDuration(self.phase_1_duration)
            self.animation.setStartValue(1.0)
            self.animation.setKeyValueAt(0.5, self.scale_percentage)
            self.animation.setEndValue(1.0)
            self.animation.setEasingCurve(self.scale_easing_style)
            logging.debug("PowAnimation set up.")
        except Exception as e:
            logging.exception("Failed to set up PowAnimation: %s", e)
