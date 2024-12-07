import sys
import logging
from typing import List

from PyQt6.QtCore import QTimer, QEasingCurve, QPointF, QUrl, Qt, pyqtSlot
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
        self.swivel_timer.start(2750)

    def start_animation(self, animation) -> None:
        """
        Starts the given animation and adds it to the appropriate active animations list.

        Args:
            animation (Animation): The animation instance to start.
        """
        try:
            animation.finished.connect(lambda: self.handle_animation_finished(animation))
            if animation:
                self.active_animations.append(animation)
                self.request_display(animation.animation_object)
                animation.start()
                logging.info("Animation started: %s", animation)
            else:
                logging.warning("Attempted to start invalid animation type: %s", type(animation))
        except Exception as e:
            logging.exception("Error in start_animation: %s", e)

    def stop_animation(self, animation) -> None:
        """
        Stops the given animation and removes it from the active animations list.

        Args:
            animation (Animation): The animation instance to stop.
        """
        try:
            animation.stop()

            if animation:
                self.clean_up_animation(animation)

            logging.info("Animation stopped: %s", animation)
        except Exception as e:
            logging.exception("Error in stop_animation: %s", e)

    def clean_up_animation(self, animation) -> None:
        """
        Cleans up the animation by removing it from active lists and deleting it safely.

        Args:
            animation (Animation): The animation instance to clean up.
        """
        try:
            removed = False
            if animation:
                if animation in self.active_animations:
                    self.active_animations.remove(animation)
                    removed = True

                if removed:
                    animation.deleteLater()
                    logging.debug("Animation cleaned up and deleted: %s", animation)
                else:
                    logging.warning("Attempted to clean up animation not found in active lists: %s", animation)
        except Exception as e:
            logging.exception("Error in clean_up_animation: %s", e)

    def request_display(self, animation_object) -> None:
        """
        Sends a request to the Overlay to display the animation.

        Args:
            animation_object (AnimationText): The animation instance's animation_object to be displayed.
        """
        try:
            if animation_object:
                self.overlay.addItem(animation_object)
                logging.debug("Animation Item added to scene: %s", animation_object)
            else:
                logging.warning("Attempted to add Animation Item to scene: %s", animation_object)
        except Exception as e:
            logging.exception("Error requesting display on overlay: %s", e)

    @pyqtSlot()
    def handle_animation_finished(self, animation) -> None:
        """
        Handles the cleanup process when an animation finishes.

        Args:
            animation (Animation): The animation instance that has started.
        """
        try:
            self.clean_up_animation(animation)
            logging.debug("Handled animation finished: %s", animation)
        except Exception as e:
            logging.exception("Error in handle_animation_finished: %s", e)

    def _create_base_animation_text(self, msg="Default Message") -> AnimationText:
        font_type = "Helvetica"
        font_size = 16
        message = msg
        icon_file = QPixmap("C:/intellij-projects/jetque/jetque/resources/test_animation_icon.jpg")
        color = QColor("white")
        outline_color = QColor("black")
        drop_shadow_color = QColor(0, 0, 0, 191)
        icon_alignment = "left"
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
        duration = 10000
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
