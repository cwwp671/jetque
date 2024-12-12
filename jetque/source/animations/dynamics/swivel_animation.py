# src/animations/dynamics/swivel_animation.py
from typing import Optional

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QSequentialAnimationGroup, QObject
from PyQt6.QtMultimedia import QSoundEffect

from jetque.source.animations.dynamics.dynamic_animation import DynamicAnimation


class SwivelAnimation(DynamicAnimation):
    """
    Handles swivel animations, moving the animation_object in two phases:
    phase 1 to the swivel position and phase 2 to the ending position.
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
            phase_1_duration: int,
            phase_2_duration: int,
            swivel_position: QPointF,
            parent=None
    ) -> None:
        """
        Initialize the SwivelAnimation with the given parameters.

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
            phase_1_duration (int): The duration of phase 1
            phase_2_duration (int): The duration of phase 2
            swivel_position (QPointF): The Swivel position for the animation.
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

        # Initialize SwivelAnimation specific attributes


        # Phase 1
        # self.removeAnimation(self.animation)  # Removes Phase 1 from Parallel Group
        # self.phase_1_duration: int = phase_1_duration
        self.swivel_position: QPointF = swivel_position
        self.animation.setKeyValueAt(0.5, self.swivel_position)
        # self.animation.setDuration(self.phase_1_duration)
        # self.animation.setEndValue(self.swivel_position)
        # Phase 2
        # self.phase_2_duration: int = phase_2_duration
        # self.animation2 = QPropertyAnimation(self.animation_object, b"pos")
        # self.animation2.setDuration(self.phase_2_duration)
        # self.animation2.setStartValue(self.swivel_position)
        # self.animation2.setEndValue(self.ending_position)
        # self.animation2.setEasingCurve(self.easing_style)
        # Phase Sequence
        # self.animation_sequence: QSequentialAnimationGroup = QSequentialAnimationGroup()
        # self.animation_sequence.addAnimation(self.animation)
        # self.animation_sequence.addAnimation(self.animation2)
        # self.addAnimation(self.animation_sequence)  # Adds the Sequence to the Parallel Group
