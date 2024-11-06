# src/animations/static_animation.py

import logging
from abc import abstractmethod

from PyQt6.QtCore import QObject, QEasingCurve, QPointF, QParallelAnimationGroup, QPropertyAnimation, \
    QSequentialAnimationGroup
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation import Animation
from src.animations.animation_label import AnimationLabel


class StaticAnimation(Animation):
    """
    Base class for static animations, handling common functionalities for static animations.

    Attributes:
        jiggle (bool): Whether the jiggle effect is enabled.
        jiggle_intensity (float): The intensity of the jiggle effect from AnimationFactory's JIGGLE_MAP.
    """

    def __init__(
            self,
            parent: QObject,
            animation_type: str,
            sound: QSoundEffect,
            duration: int,
            starting_position: QPointF,
            fade_in: bool,
            fade_out: bool,
            fade_in_percentage: float,
            fade_out_percentage: float,
            fade_in_easing_style: QEasingCurve.Type,
            fade_out_easing_style: QEasingCurve.Type,
            label: AnimationLabel,
            jiggle: bool,
            jiggle_intensity: float
    ) -> None:
        """
        Initialize the StaticAnimation with the given parameters.

        Args:
            parent (QObject): The parent object.
            animation_type (str): The type of animation.
            sound (QSoundEffect): The sound effect to play.
            duration (int): The duration of the animation in milliseconds.
            starting_position (QPointF): The starting position of the animation.
            fade_in (bool): Whether the animation fades in.
            fade_out (bool): Whether the animation fades out.
            fade_in_percentage (float): The percentage of duration for fade-in.
            fade_out_percentage (float): The percentage of duration for fade-out.
            fade_in_easing_style (QEasingCurve.Type): The easing curve for fade-in.
            fade_out_easing_style (QEasingCurve.Type): The easing curve for fade-out.
            label (AnimationLabel): The label associated with the animation.
            jiggle (bool): Whether the jiggle effect is enabled.
            jiggle_intensity (float): The intensity of the jiggle effect.
        """
        self.jiggle: bool = jiggle
        self.jiggle_intensity: float = jiggle_intensity
        super().__init__(
            parent=parent,
            animation_type=animation_type,
            sound=sound,
            duration=duration,
            starting_position=starting_position,
            fade_in=fade_in,
            fade_out=fade_out,
            fade_in_percentage=fade_in_percentage,
            fade_out_percentage=fade_out_percentage,
            fade_in_easing_style=fade_in_easing_style,
            fade_out_easing_style=fade_out_easing_style,
            label=label
        )
        logging.debug("StaticAnimation initialized.")

    @abstractmethod
    def play(self) -> None:
        """
        Start the static animation.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the static animation.
        Must be implemented by subclasses.
        """
        pass

    def setup_animations(self) -> None:
        """
        Set up the static animation settings and groups.
        """
        logging.debug("Setting up StaticAnimation animations.")
        try:
            super().setup_animations()
            logging.debug("StaticAnimation animations set up.")
        except Exception as e:
            logging.exception("Error setting up StaticAnimation animations: %s", e)

    def _apply_jiggle(self) -> None:
        """
        Manipulate the position with jiggle effect.
        """
        # Implement logic when ready to handle jiggle effect
        pass

    def _connect_signals(self) -> None:
        """
        Connect any necessary static animation signals to handlers.
        """
        try:
            super()._connect_signals()
            self.animation_group.finished.connect(self.finished.emit)
            logging.debug("Signals connected for StaticAnimation")
        except Exception as e:
            logging.exception("Failed to connect signals: %s", e)

    def _connect_slots(self) -> None:
        """
        Connect any necessary static animation slots to handlers.
        """
        try:
            super()._connect_slots()
            logging.debug("Slots connected for StaticAnimation")
        except Exception as e:
            logging.exception("Failed to connect slots: %s", e)
