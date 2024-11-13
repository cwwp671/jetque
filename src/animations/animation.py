# src/animations/animation.py

import logging

from PyQt6.QtCore import (
    QEasingCurve, QPointF, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QAbstractAnimation
)

from PyQt6.QtMultimedia import QSoundEffect
from src.animations.animation_text_item import AnimationTextItem


class Animation(QParallelAnimationGroup):
    """
    Base class for all animations.
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
            parent: The parent object.
        """
        super().__init__(parent)
        self.type: str = animation_type
        self.sound: QSoundEffect = sound
        self.label: AnimationTextItem = label
        self.duration: int = duration
        self.starting_position: QPointF = starting_position
        self.fade_in: bool = fade_in
        self.fade_in_duration: int = fade_in_duration
        self.fade_in_easing_style: QEasingCurve.Type = fade_in_easing_style
        self.fade_out: bool = fade_out
        self.fade_out_duration: int = fade_out_duration
        self.fade_out_delay: int = fade_out_delay
        self.fade_out_easing_style: QEasingCurve.Type = fade_out_easing_style
        self.animation: QPropertyAnimation = QPropertyAnimation(self.label, b"pos")

        if self.fade_in:
            self.fade_in_animation: QPropertyAnimation = QPropertyAnimation(self.label, b"opacity")

        if self.fade_out:
            self.fade_out_animation: QPropertyAnimation = QPropertyAnimation(self.label, b"opacity")
            self.fade_out_group: QSequentialAnimationGroup = QSequentialAnimationGroup()

        self.finished.connect(self._on_finished)

        logging.debug("Animation initialized: Type=%s", self.type)

    def start(self, policy=QAbstractAnimation.DeletionPolicy.DeleteWhenStopped) -> None:
        """
        Start the animation.

        :param policy: Deletion policy for the animation.
        """
        try:
            super().start(policy)
            self._play_sound()
            logging.debug("Animation started.")
            logging.debug(f"Label Pos: {self.label.pos()}")
            logging.debug(f"Label Scene Pos: {self.label.scenePos()}")
        except Exception as e:
            logging.exception("Failed to start Animation: %s", e)

    def stop(self) -> None:
        """
        Stop the animation.
        """
        try:
            super().stop()
            logging.debug("Animation stopped.")
        except Exception as e:
            logging.exception("Failed to stop Animation: %s", e)

    def _setup_animations(self) -> None:
        """
        Set up the animation settings and groups.
        """
        try:
            if self.fade_in:
                self.fade_in_animation.setDuration(self.fade_in_duration)
                self.fade_in_animation.setStartValue(0.0)
                self.fade_in_animation.setEndValue(1.0)
                self.fade_in_animation.setEasingCurve(self.fade_in_easing_style)
                self.addAnimation(self.fade_in_animation)
                logging.debug(f"Fade In Created:\n"
                              f"Duration: {self.fade_in_animation.duration()}\n"
                              f"Starting Opacity: {self.fade_in_animation.startValue()}\n"
                              f"Ending Opacity: {self.fade_in_animation.endValue()}\n"
                              f"Easing Curve: {self.fade_in_animation.easingCurve()}")

            if self.fade_out:
                self.fade_out_animation.setDuration(self.fade_out_duration)
                self.fade_out_animation.setStartValue(1.0)
                self.fade_out_animation.setEndValue(0.0)
                self.fade_out_animation.setEasingCurve(self.fade_out_easing_style)
                self.fade_out_group.addPause(self.fade_out_delay)
                self.fade_out_group.addAnimation(self.fade_out_animation)
                self.addAnimation(self.fade_out_group)
                logging.debug(f"Fade Out Created:\n"
                              f"Duration: {self.fade_out_animation.duration()}\n"
                              f"Pause Duration: {self.fade_out_delay}\n"
                              f"Starting Opacity: {self.fade_out_animation.startValue()}\n"
                              f"Ending Opacity: {self.fade_out_animation.endValue()}\n"
                              f"Easing Curve: {self.fade_out_animation.easingCurve()}"
                              )

            self.animation.setDuration(self.duration)
            self.animation.setStartValue(self.starting_position)
            self.addAnimation(self.animation)
            logging.debug(f"Animation Created:\n"
                          f"Duration: {self.animation.duration()}\n"
                          f"Starting Position: {self.animation.startValue()}")
        except Exception as e:
            logging.exception("Error setting up Animation: %s", e)

    def _play_sound(self) -> None:
        """
        Play the associated sound effect if available.
        """
        if not self.sound:
            logging.debug("No sound effect to play for Animation.")
            return

        try:
            self.sound.play()
            logging.debug("Sound played for Animation.")
        except Exception as e:
            logging.exception("Error playing sound for Animation: %s", e)

    def _on_finished(self):
        """
        Slot called when the animation finishes.
        """
        logging.debug("Animation finished.")
        if self.label:
            # Remove the label from the scene
            scene = self.label.scene()
            if scene:
                scene.removeItem(self.label)
                logging.debug("Label removed from scene.")
            self.label.deleteLater()
            logging.debug("Label scheduled for deletion.")
        self.deleteLater()
