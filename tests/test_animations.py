import sys
import logging
from typing import List

from PyQt6.QtCore import QTimer, QEasingCurve, QPointF, QUrl, Qt, pyqtSlot, QAbstractAnimation
from PyQt6.QtGui import QFont, QPen, QColor, QPixmap
from PyQt6.QtMultimedia import QSoundEffect

from jetque.jetque import JetQue
from jetque.source.animations.animation import Animation
from jetque.source.animations.animation_font import AnimationFont
from jetque.source.animations.animation_text import AnimationText
from jetque.source.animations.dynamics.directional_animation import DirectionalAnimation
from jetque.source.animations.dynamics.parabola_animation import ParabolaAnimation
from jetque.source.animations.dynamics.swivel_animation import SwivelAnimation
from jetque.source.animations.statics.pow_animation import PowAnimation
from jetque.source.animations.statics.stationary_animation import StationaryAnimation
from jetque.source.animations.animation_point_f import AnimationPointF


class AnimationTester(JetQue):
    def __init__(self, sys_argv: List[str]) -> None:
        super().__init__(sys_argv)
        self.overlay.setParent(self)
        self.active_animations = []
        self.pow_timer = QTimer(self)
        self.pow_timer.timeout.connect(self.run_pow_animation_test)
        self.pow_timer.start(5250)
        self.swivel_timer = QTimer(self)
        self.swivel_timer.timeout.connect(self.run_swivel_animation_test)
        self.swivel_timer.start(500)

    def start_animation(self, animation) -> None:
        """
        Starts the given animation and adds it to the appropriate active animations list.

        Args:
            animation (Animation): The animation instance to start.
        """
        try:
            if animation and animation.animation_object:

                def animation_cleanup():
                    self.animation_cleanup(animation, animation.animation_object)

                animation.finished.connect(animation_cleanup)
                self.active_animations.append(animation)
                self.overlay.addItem(animation.animation_object)
                animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
                # logging.debug("Animation started: %s", animation)
        except Exception as e:
            logging.exception("Exception in start_animation: %s", e)

    @pyqtSlot()
    def animation_cleanup(self, animation, animation_object) -> None:
        """
        Handles the cleanup process when an animation finishes.

        Args:
            animation (Animation): The animation instance that has started.
            animation_object (AnimationText): The object being animated.
        """
        try:
            if animation and animation_object and animation in self.active_animations:
                # logging.debug(f"Starting animation_cleanup on animation: {animation} "
                #               f"and animation_object: {animation_object}")
                # logging.debug("Removing animation from active_animations list")
                self.active_animations.remove(animation)
                # logging.debug("Disconnecting animation finished signal")
                animation.finished.disconnect()
                # logging.debug("Queuing deletion on animation_object")
                animation_object.deleteLater()

                # We are using a DeletionPolicy when starting our animation, so this is for reference only
                # logging.debug("Queuing deletion on animation")
                # animation.deleteLater()

                # logging.debug("Finished animation_cleanup")
        except Exception as e:
            logging.exception("Exception in animation_cleanup: %s", e)

    def _create_base_animation_text(self, msg="Default Message") -> AnimationText:
        font_type = "Helvetica"
        font_size = 36
        message = msg
        icon_file = QPixmap("C:/intellij-projects/jetque/jetque/resources/test_animation_icon.png")
        color = QColor("white")
        outline_color = QColor("black")
        drop_shadow_color = QColor(0, 0, 0, 191)
        icon_alignment = "right"
        icon_on = True
        outline_on = True
        drop_shadow_on = True
        italics_on = False
        kerning_on = True
        overline_on = False
        strikethrough_on = False
        underline_on = False
        extra_letter_spacing = 0.0
        extra_word_spacing = 0.0
        outline_width = 2.0
        drop_shadow_radius = 7.0
        drop_shadow_offset = QPointF(-3.5, 6.1)
        outline_type = Qt.PenStyle.SolidLine
        outline_shape = Qt.PenCapStyle.FlatCap
        outline_corners = Qt.PenJoinStyle.BevelJoin
        weight = QFont.Weight.Normal
        capitalization = QFont.Capitalization.MixedCase
        stretch = QFont.Stretch.Unstretched

        text_font = AnimationFont(
            font_type=font_type,
            font_size=font_size,
            font_weight=weight,
            font_capitalization=capitalization,
            font_stretch=stretch,
            font_letter_spacing=extra_letter_spacing,
            font_word_spacing=extra_word_spacing,
            font_italic=italics_on,
            font_kerning=kerning_on,
            font_overline=overline_on,
            font_strikethrough=strikethrough_on,
            font_underline=underline_on
        )

        text_outline_pen = QPen(
            outline_color,
            outline_width,
            outline_type,
            outline_shape,
            outline_corners
        )

        text_item = AnimationText(
            text_font=text_font,
            text_message=message,
            text_color=color,
            outline=outline_on,
            outline_pen=text_outline_pen,
            drop_shadow=drop_shadow_on,
            drop_shadow_offset=drop_shadow_offset,
            drop_shadow_blur_radius=drop_shadow_radius,
            drop_shadow_color=drop_shadow_color,
            icon=icon_on,
            icon_pixmap=icon_file,
            icon_alignment=icon_alignment,
            parent=self.overlay
        )

        return text_item

    @staticmethod
    def _create_sound_effect() -> QSoundEffect:
        sound = QSoundEffect()
        sound.setSource(QUrl())  # Fake sound file
        return sound

    def run_directional_animation_test(self):
        starting_pos = QPointF()
        ending_pos = QPointF()
        anim_text = self._create_base_animation_text()

        anim = DirectionalAnimation(
            animation_type="Directional",
            sound=self._create_sound_effect(),
            duration=1000,
            starting_position=starting_pos,
            fade_in=True,
            fade_out=True,
            fade_in_duration=250,
            fade_out_duration=250,
            fade_out_delay=250,
            fade_in_easing_style=QEasingCurve.Type.OutQuad,
            fade_out_easing_style=QEasingCurve.Type.InQuad,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.Linear,
        )

        self.start_animation(anim)

    def run_parabola_animation_test(self):
        starting_pos = QPointF()
        ending_pos = QPointF()
        parabola_points = [
            AnimationPointF((starting_pos.x() + ending_pos.x()) / 2, starting_pos.y() - 100, 0.5),
        ]
        anim_text = self._create_base_animation_text()

        anim = ParabolaAnimation(
            animation_type="Parabola",
            sound=self._create_sound_effect(),
            duration=1500,
            starting_position=starting_pos,
            fade_in=True,
            fade_out=True,
            fade_in_duration=250,
            fade_out_duration=250,
            fade_out_delay=250,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.Linear,
            parabola_points=parabola_points
        )

        self.start_animation(anim)

    def run_swivel_animation_test(self):
        starting_pos = QPointF(1280.0, 700.0)
        swivel_pos = QPointF(1920.0, 350.0)
        ending_pos = QPointF(2560.0, 350.0)
        duration = 3000
        fade_in_duration = int(duration * 0.1)
        fade_out_duration = int(duration * 0.1)
        fade_out_delay = int(duration - fade_out_duration)
        phase_1_duration = int(duration / 2)
        phase_2_duration = int(duration / 2)
        fade_in_on = True
        fade_out_on = True
        anim_text = self._create_base_animation_text("Swivel")

        anim = SwivelAnimation(
            animation_type="Swivel",
            sound=self._create_sound_effect(),
            duration=duration,
            starting_position=starting_pos,
            fade_in=fade_in_on,
            fade_out=fade_out_on,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration,
            fade_out_delay=fade_out_delay,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.InQuad,
            phase_1_duration=phase_1_duration,
            phase_2_duration=phase_2_duration,
            swivel_position=swivel_pos,
        )

        self.start_animation(anim)

    def run_pow_animation_test(self):
        starting_pos = QPointF(1280.0, 350.0)  # Manual start pos
        duration = 5000
        fade_in_duration = int(duration * 0.1)
        fade_out_duration = int(duration * 0.1)
        fade_out_delay = int(duration - fade_out_duration)
        phase_1_duration = int(duration * 0.05)
        phase_2_duration = int(duration * 0.95)
        jiggle_intensity = 25
        scale_increase_percentage = 2.75
        jiggle_on = True
        fade_in_on = True
        fade_out_on = True

        anim_text = self._create_base_animation_text("Pow")

        anim = PowAnimation(
            animation_type="Pow",
            sound=self._create_sound_effect(),
            duration=duration,
            starting_position=starting_pos,
            fade_in=fade_in_on,
            fade_out=fade_out_on,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration,
            fade_out_delay=fade_out_delay,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            jiggle=jiggle_on,
            jiggle_intensity=jiggle_intensity,
            scale_percentage=scale_increase_percentage,
            scale_easing_style=QEasingCurve.Type.OutInQuad,
            phase_1_duration=phase_1_duration,
            phase_2_duration=phase_2_duration
        )

        self.start_animation(anim)

    def run_stationary_animation_test(self):
        starting_pos = QPointF()
        anim_text = self._create_base_animation_text()

        anim = StationaryAnimation(
            animation_type="Stationary",
            sound=self._create_sound_effect(),
            duration=1000,
            starting_position=starting_pos,
            fade_in=True,
            fade_out=True,
            fade_in_duration=250,
            fade_out_duration=250,
            fade_out_delay=250,
            fade_in_easing_style=QEasingCurve.Type.OutQuad,
            fade_out_easing_style=QEasingCurve.Type.InQuad,
            animation_object=anim_text,
            jiggle=True,
            jiggle_intensity=100
        )

        self.start_animation(anim)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    app = AnimationTester(sys.argv)
    app.run()
