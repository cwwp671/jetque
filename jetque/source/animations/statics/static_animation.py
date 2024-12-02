# src/animations/static_animation.py

import logging
import random

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation
from PyQt6.QtMultimedia import QSoundEffect

from jetque.source.animations.animation import Animation
from jetque.source.animations.animation_text import AnimationText

# Constants
JIGGLE_AMOUNT = 1.0
INFINITE_LOOP = -1


class StaticAnimation(Animation):
    """
    Base class for static animations, handling common functionalities including
    an optional jiggle effect.

    Attributes:
        jiggle (bool): Whether the jiggle effect is enabled.
        jiggle_intensity (int): The intensity of the jiggle effect in milliseconds.
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
            jiggle: bool,
            jiggle_intensity: int,
            parent=None
    ) -> None:
        """
        Initialize the StaticAnimation with the given parameters.

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
            parent=parent
        )

        self.jiggle: bool = jiggle

        # Optional Jiggle effect
        if self.jiggle:
            self.jiggle_intensity: int = jiggle_intensity
            self.old_position: QPointF = self.starting_position
            self.jiggle_animation: QPropertyAnimation = QPropertyAnimation(self.animation_object, b"pos")
            self.jiggle_animation.currentLoopChanged.connect(self._apply_jiggle)
            self.jiggle_animation.setDuration(self.jiggle_intensity)
            self.jiggle_animation.setLoopCount(INFINITE_LOOP)
            self.jiggle_animation.setStartValue(self.starting_position)
            self.jiggle_animation.setEndValue(self.starting_position)
            self.addAnimation(self.jiggle_animation)

    def _apply_jiggle(self) -> None:
        """
        Apply a random jiggle effect to the AnimationTextItem position.
        """
        try:
            new_position: QPointF = QPointF(
                self.animation_object.x() + random.uniform(-JIGGLE_AMOUNT, JIGGLE_AMOUNT),
                self.animation_object.y() + random.uniform(-JIGGLE_AMOUNT, JIGGLE_AMOUNT)
            )
            self.old_position = self.animation_object.pos()
            self.jiggle_animation.setStartValue(self.old_position)
            self.jiggle_animation.setEndValue(new_position)
        except Exception as e:
            logging.exception("Error handling jiggle loop change: %s", e)
