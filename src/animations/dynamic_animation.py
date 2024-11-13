# src/animations/dynamic_animation.py

import logging

from PyQt6.QtCore import QEasingCurve, QPointF
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation import Animation
from src.animations.animation_text_item import AnimationTextItem


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
            label: AnimationTextItem,
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
            label (AnimationTextItem): The label associated with the animation.
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
            label=label,
            parent=parent
        )

        self.ending_position: QPointF = ending_position
        self.easing_style: QEasingCurve.Type = easing_style

    def _setup_animations(self) -> None:
        """
        Set up the dynamic animation settings and groups.
        """
        try:
            super()._setup_animations()
            self.animation.setEndValue(self.ending_position)
            self.animation.setEasingCurve(self.easing_style)
            logging.debug(f"DynamicAnimation Created:\n"
                          f"Ending Position: {self.animation.endValue()}\n"
                          f"Easing Curve: {self.animation.easingCurve()}")
        except Exception as e:
            logging.exception("Error setting up DynamicAnimation: %s", e)
