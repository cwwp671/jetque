# src/animations/dynamics/parabola_animation.py

from typing import List

from PyQt6.QtCore import QEasingCurve, QPointF
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation_point_f import AnimationPointF
from src.animations.animation_text import AnimationText
from src.animations.dynamic_animation import DynamicAnimation


class ParabolaAnimation(DynamicAnimation):
    """
    Handles parabolic animations, moving the label along a parabolic path
    from the starting position to the ending position based on the specified direction.
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
            ending_position: QPointF,
            easing_style: QEasingCurve.Type,
            parabola_points: List[AnimationPointF],
            parent=None
    ) -> None:
        """
        Initialize the ParabolaAnimation with the given parameters.

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
            ending_position (QPointF): The ending position of the animation.
            easing_style (QEasingCurve.Type): The easing curve type for the animation.
            parabola_points (List[AnimationPointF]): The positions along the curve of the animation.
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
            ending_position=ending_position,
            easing_style=easing_style,
            parent=parent
        )

        # Initialize ParabolaAnimation specific attributes
        self.parabola_points: List[AnimationPointF] = parabola_points

        for point in self.parabola_points:
            self.animation.setKeyValueAt(point.key_value, point)
