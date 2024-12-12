# src/animations/dynamics/parabola_animation.py

from typing import List, Optional

from PyQt6.QtCore import QEasingCurve, QPointF, QObject
from PyQt6.QtMultimedia import QSoundEffect

from jetque.source.animations.dynamics.dynamic_animation import DynamicAnimation


class ParabolaAnimation(DynamicAnimation):
    """
    Handles parabolic animations, moving the animation_object along a parabolic path
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
            animation_object: Optional[QObject],
            ending_position: QPointF,
            easing_style: QEasingCurve.Type,
            parabola_points: Optional[List[QPointF]],
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
            animation_object (Optional[QObject]): The object associated with the animation.
            ending_position (QPointF): The ending position of the animation.
            easing_style (QEasingCurve.Type): The easing curve type for the animation.
            parabola_points (Optional[List[QPointF]]): The positions along the curve of the animation.
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
            ending_position=ending_position,
            easing_style=easing_style,
            parent=parent
        )

        # Initialize ParabolaAnimation specific attributes
        self.parabola_points: Optional[List[QPointF]] = parabola_points

        for i, point in enumerate(self.parabola_points):
            t = i / (len(self.parabola_points) - 1)  # Normalized time (0 to 1)
            self.animation.setKeyValueAt(t, point)
