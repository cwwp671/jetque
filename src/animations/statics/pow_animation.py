# src/animations/statics/pow_animation.py

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QSequentialAnimationGroup, QPauseAnimation
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation_text import AnimationText
from src.animations.static_animation import StaticAnimation


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
            text_object: AnimationText,
            jiggle: bool,
            jiggle_intensity: int,
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
            text_object (AnimationText): The label associated with the animation.
            jiggle (bool): Whether the jiggle effect is enabled.
            jiggle_intensity (int): The intensity of the jiggle effect in milliseconds.
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
            text_object=text_object,
            jiggle=jiggle,
            jiggle_intensity=jiggle_intensity,
            parent=parent
        )

        # Initialize PowAnimation specific attributes
        self.scale_percentage: float = scale_percentage
        self.scale_easing_style: QEasingCurve.Type = scale_easing_style
        self.phase_1_duration: int = phase_1_duration
        self.phase_2_duration: int = phase_2_duration
        self.scale_animation = QPropertyAnimation(self.label, b"pos")
        self.scale_animation.setDuration(self.phase_1_duration)
        self.scale_animation.setStartValue(1.0)
        self.scale_animation.setKeyValueAt(0.5, self.scale_percentage)
        self.scale_animation.setEndValue(1.0)
        self.scale_animation.setEasingCurve(self.scale_easing_style)
        self.addAnimation(self.scale_animation)
        # Delay the Optional Jiggle to be after the scaling effect finishes
        if self.jiggle:
            self.removeAnimation(self.jiggle_animation)
            self.jiggle_pause_animation: QPauseAnimation = QPauseAnimation(self.phase_1_duration, self.label)
            self.jiggle_animation_sequence: QSequentialAnimationGroup = QSequentialAnimationGroup()
            self.jiggle_animation_sequence.addAnimation(self.jiggle_pause_animation)
            self.jiggle_animation_sequence.addAnimation(self.jiggle_animation)
            self.addAnimation(self.jiggle_animation_sequence)
