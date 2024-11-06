# src/animations/statics/stationary_animation.py

import logging
from typing import Any

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.static_animation import StaticAnimation
from src.animations.animation_label import AnimationLabel


class StationaryAnimation(StaticAnimation):
    """
    Represents a stationary animation with no movement but may include other effects like fade in/out.
    """

    def __init__(
            self,
            parent: Any,
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
        Initialize the StationaryAnimation with the given parameters.

        Args:
            parent (Any): The parent object.
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
            label=label,
            jiggle=jiggle,
            jiggle_intensity=jiggle_intensity
        )
        logging.debug("StationaryAnimation initialized.")

    def play(self) -> None:
        """
        Start the stationary animation.
        """
        logging.info("Playing StationaryAnimation.")
        try:
            self.play_sound()
            self.label.show()
            self.animation_group.start()
            logging.debug("StationaryAnimation started.")
        except Exception as e:
            logging.exception("Failed to play StationaryAnimation: %s", e)

    def stop(self) -> None:
        """
        Stop the stationary animation.
        """
        logging.info("Stopping StationaryAnimation.")
        try:
            self.animation_group.stop()
            logging.debug("StationaryAnimation stopped.")
        except Exception as e:
            logging.exception("Failed to stop StationaryAnimation: %s", e)

    def setup_animations(self) -> None:
        """
        Set up the stationary animation settings and groups.
        """
        logging.debug("Setting up StationaryAnimation animations.")
        try:
            self.animation.setDuration(self.duration)
            self.animation.setStartValue(self.starting_position)
            self.animation.setEndValue(self.starting_position)
            self.animation_group.addAnimation(self.animation)
            logging.debug("StationaryAnimation animations set up.")
            super().setup_animations()
        except Exception as e:
            logging.exception("Error setting up StationaryAnimation animations: %s", e)

    def _connect_signals(self) -> None:
        """
        Connect signals specific to StationaryAnimation.
        """
        logging.debug("Connecting StationaryAnimation signals.")
        try:
            super()._connect_signals()
            # Connect any StationaryAnimation-specific signals here
            logging.debug("StationaryAnimation signals connected.")
        except Exception as e:
            logging.exception("Failed to connect StationaryAnimation signals: %s", e)

    def _connect_slots(self) -> None:
        """
        Connect slots specific to StationaryAnimation.
        """
        logging.debug("Connecting StationaryAnimation slots.")
        try:
            super()._connect_slots()
            # Connect any StationaryAnimation-specific slots here
            logging.debug("StationaryAnimation slots connected.")
        except Exception as e:
            logging.exception("Failed to connect StationaryAnimation slots: %s", e)
