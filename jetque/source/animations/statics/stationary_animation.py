# src/animations/statics/stationary_animation.py
from typing import Optional

from PyQt6.QtCore import QEasingCurve, QPointF, QObject
from PyQt6.QtMultimedia import QSoundEffect

from jetque.source.animations.statics.static_animation import StaticAnimation


class StationaryAnimation(StaticAnimation):
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
            animation_object: Optional[QObject],
            jiggle: bool,
            jiggle_intensity: int,
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
            animation_object (Optional[QObject]): The object associated with the animation.
            jiggle (bool): Whether the jiggle effect is enabled.
            jiggle_intensity (int): The intensity of the jiggle effect in milliseconds.
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
            jiggle=jiggle,
            jiggle_intensity=jiggle_intensity,
            parent=parent
        )
