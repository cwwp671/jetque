# src/animations/dynamic_animation.py

import logging
from abc import abstractmethod
from typing import Tuple

from PyQt6.QtCore import QObject, QEasingCurve, QPointF
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation import Animation
from src.animations.animation_label import AnimationLabel


class DynamicAnimation(Animation):
    """
    Base class for dynamic animations, handling common functionalities for dynamic animations.

    Attributes:
        direction (Tuple[float, float]):
            Direction[0] (x), Direction[1] (y)
            multiplier from AnimationFactory's DIRECTION_MAP.
        ending_position (QPointF): The ending position of the animation.
        easing_style (QEasingCurve.Type): The easing curve type for the animation.
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
            ending_position: QPointF,
            direction: Tuple[float, float],
            easing_style: QEasingCurve.Type
    ) -> None:
        """
        Initialize the DynamicAnimation with the given parameters.

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
            ending_position (QPointF): The ending position of the animation.
            direction (Tuple[float, float]):
                Direction[0] (x), Direction[1] (y)
                multiplier from AnimationFactory's DIRECTION_MAP.
            easing_style (QEasingCurve.Type): The easing curve type for the animation.
        """
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
        self.direction: Tuple[float, float] = direction
        self.ending_position: QPointF = ending_position
        self.easing_style: QEasingCurve.Type = easing_style

        # Initializes any dynamic-specific attributes
        logging.debug(
            "DynamicAnimation initialized with ending_position=%s, "
            "horizontal_direction=%d, vertical_direction=%d, easing_style=%s",
            self.ending_position,
            self.direction[0],
            self.direction[1],
            self.easing_style.name
        )

    @abstractmethod
    def play(self) -> None:
        """
        Start the dynamic animation.
        """
        # Implement common logic or override in subclasses
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the dynamic animation.
        """
        # Implement common logic or override in subclasses
        pass

    @abstractmethod
    def setup_animations(self) -> None:
        """
        Set up the dynamic animations.
        """
        # Implement common logic or override in subclasses
        pass

    def _connect_signals(self) -> None:
        """
        Connect any necessary dynamic animation signals to handlers.
        """
        try:
            super()._connect_signals()
            logging.debug("Signals connected for DynamicAnimation")
        except Exception as e:
            logging.exception("Failed to connect signals: %s", e)

    def _connect_slots(self) -> None:
        """
        Connect any necessary dynamic animation slots to handlers.
        """
        try:
            super()._connect_slots()
            logging.debug("Slots connected for DynamicAnimation")
        except Exception as e:
            logging.exception("Failed to connect slots: %s", e)
