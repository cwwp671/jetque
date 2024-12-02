# src/animations/dynamic_animation.py

from PyQt6.QtCore import QEasingCurve, QPointF
from PyQt6.QtMultimedia import QSoundEffect

from jetque.source.animations.animation import Animation
from jetque.source.animations.animation_text import AnimationText


class DynamicAnimation(Animation):
    """
    Base class for dynamic animations, handling common functionalities for dynamic animations.

    Attributes:
        ending_position (QPointF): The ending position of the animation.
        easing_style (QEasingCurve.Type): The easing curve type for the animation.
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
            animation_object: AnimationText,
            ending_position: QPointF,
            easing_style: QEasingCurve.Type,
            parent=None
    ) -> None:
        """
        Initialize the DynamicAnimation with the given parameters.

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
            animation_object (AnimationText): The object associated with the animation.
            ending_position (QPointF): The ending position of the animation.
            easing_style (QEasingCurve.Type): The easing curve type for the animation.
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
            animation_object=animation_object,
            parent=parent
        )

        # Initialize common attributes between all DynamicAnimation children
        self.ending_position: QPointF = ending_position
        self.easing_style: QEasingCurve.Type = easing_style
        self.animation.setEndValue(self.ending_position)
        self.animation.setEasingCurve(self.easing_style)
