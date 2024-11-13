# src/animations/dynamics/swivel_animation.py

import logging

from PyQt6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QSequentialAnimationGroup
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation_text_item import AnimationTextItem
from src.animations.dynamic_animation import DynamicAnimation


class SwivelAnimation(DynamicAnimation):
    """
    Handles swivel animations, moving the label in two phases:
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
            label: AnimationTextItem,
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
            label (AnimationTextItem): The label associated with the animation.
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
            label=label,
            ending_position=ending_position,
            easing_style=easing_style,
            parent=parent
        )

        self.phase_1_duration: int = phase_1_duration
        self.phase_2_duration: int = phase_2_duration
        self.swivel_position: QPointF = swivel_position
        self.animation2 = QPropertyAnimation(self.label, b"pos")
        self.animation_sequence: QSequentialAnimationGroup = QSequentialAnimationGroup()
        self._setup_animations()

    def _setup_animations(self) -> None:
        """
        Set up the swivel animation settings and groups.
        """
        try:
            super()._setup_animations()
            self.animation.setDuration(self.phase_1_duration)
            self.animation.setStartValue(self.starting_position)
            self.animation.setEndValue(self.swivel_position)
            self.animation.setEasingCurve(self.easing_style)
            logging.debug(f"SwivelAnimation Created:\n"
                          f"Duration: {self.animation.duration()}\n"
                          f"Swivel Position: {self.animation.endValue()}")
            self.animation2.setDuration(self.phase_2_duration)
            self.animation2.setStartValue(self.swivel_position)
            self.animation2.setEndValue(self.ending_position)
            self.animation2.setEasingCurve(self.easing_style)
            logging.debug(f"SwivelAnimation Phase 2 Created:\n"
                          f"Duration: {self.animation2.duration()}\n"
                          f"Starting Position: {self.animation2.startValue()}\n"
                          f"Ending Position: {self.animation2.endValue()}\n"
                          f"Easing Curve: {self.animation2.easingCurve()}")
            self.removeAnimation(self.animation)
            self.animation_sequence.addAnimation(self.animation)
            self.animation_sequence.addAnimation(self.animation2)
            self.addAnimation(self.animation_sequence)
            logging.debug("Animation Fully Set Up")
            logging.debug(f"Label Pos: {self.label.pos()}")
            logging.debug(f"Label Pos: {self.label.scenePos()}")
        except Exception as e:
            logging.exception("Failed to set up SwivelAnimation: %s", e)
