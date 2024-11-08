# src/animations/static_animation.py

import logging
import random

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation import Animation
from src.animations.animation_label import AnimationLabel

# Constants
JIGGLE_AMOUNT = 1.0
INFINITE_LOOP = -1


class StaticAnimation(Animation):
    """
    Base class for static animations, handling common functionalities including
    an optional jiggle effect.

    Attributes:
        jiggle (bool): Whether the jiggle effect is enabled.
        jiggle_intensity (float): The intensity of the jiggle effect in milliseconds.
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
            label (AnimationLabel): The label associated with the animation.
            jiggle (bool): Whether the jiggle effect is enabled.
            jiggle_intensity (float): The intensity of the jiggle effect.
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

        self.jiggle: bool = jiggle

        if self.jiggle:
            self.jiggle_intensity: float = jiggle_intensity
            self.jiggle_animation: QPropertyAnimation = QPropertyAnimation(self.label, b"pos")
            self.jiggle_start_override: bool = False
            self.jiggle_animation.currentLoopChanged.connect(self._apply_jiggle)
            self.old_position: QPointF = self.starting_position

        logging.debug("StaticAnimation initialized.")

    def _setup_animations(self) -> None:
        """
        Set up the static animation settings and groups, including the jiggle effect.
        """
        logging.debug("Setting up StaticAnimation.")
        try:
            if self.jiggle:
                logging.debug("Jiggle effect enabled.")
                self._configure_jiggle_animation()

            logging.debug("StaticAnimation set up.")
            super()._setup_animations()
        except Exception as e:
            logging.exception("Error setting up StaticAnimation: %s", e)

    def _configure_jiggle_animation(self) -> None:
        """
        Configure the jiggle animation.
        """
        try:
            self.jiggle_animation.setDuration(int(self.jiggle_intensity))
            self.jiggle_animation.setLoopCount(INFINITE_LOOP)
            self.jiggle_animation.setStartValue(self.starting_position)
            self.jiggle_animation.setEndValue(self.starting_position)

            if not self.jiggle_start_override:
                self.addAnimation(self.jiggle_animation)

            logging.debug("Jiggle configured.")
        except Exception as e:
            logging.exception("Error configuring jiggle: %s", e)

    def _apply_jiggle(self) -> None:
        """
        Apply a random jiggle effect to the AnimationLabel position.
        """
        try:
            new_position: QPointF = QPointF(
                self.label.x() + random.uniform(-JIGGLE_AMOUNT, JIGGLE_AMOUNT),
                self.label.y() + random.uniform(-JIGGLE_AMOUNT, JIGGLE_AMOUNT)
            )
            self.old_position = self.label.pos()
            self.jiggle_animation.setStartValue(self.old_position)
            self.jiggle_animation.setEndValue(new_position)
            logging.debug("Jiggle loop changed: Starting new jiggle cycle.")
        except Exception as e:
            logging.exception("Error handling jiggle loop change: %s", e)
