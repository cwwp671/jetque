import sys
import logging
import weakref
from typing import List

from PyQt6.QtCore import QTimer, QEasingCurve, QPointF, QUrl, Qt
from PyQt6.QtGui import QFont, QPen, QColor, QPixmap

from jetque.jetque import JetQue
from jetque.source.animations.animation_font import AnimationFont
from jetque.source.animations.animation_text import AnimationText
from jetque.source.animations.dynamics.directional_animation import DirectionalAnimation
from jetque.source.animations.dynamics.parabola_animation import ParabolaAnimation
from jetque.source.animations.dynamics.swivel_animation import SwivelAnimation
from jetque.source.animations.statics.pow_animation import PowAnimation
from jetque.source.animations.statics.stationary_animation import StationaryAnimation
from jetque.source.animations.animation_point_f import AnimationPointF
from PyQt6.QtMultimedia import QSoundEffect


class AnimationTester(JetQue):
    def __init__(self, sys_argv: List[str]) -> None:
        super().__init__(sys_argv)
        # Set up anchor positions

        # self.overlay.anchor_points[0].start_circle.setPos(1280.0, 700.0)
        # self.overlay.anchor_points[0].end_circle.setPos(2560.0, 700.0)
        # self.overlay.anchor_points[0].start_text.update_position()
        # self.overlay.anchor_points[0].end_text.update_position()
        # self.overlay.run_mode()

        self.overlay.setParent(self)

        # We will store animations to ensure we can check memory later
        self.active_animations = []

    def _create_base_animation_text(self) -> AnimationText:

        font_type = "Helvetica"
        font_size = 16
        message = "Default Message"
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
        # Just create a dummy sound effect (no actual sound)
        sound = QSoundEffect()
        sound.setSource(QUrl())  # No actual sound file
        return sound

    def _get_starting_position(self) -> QPointF:
        # For the anchor, the start circle is the "Incoming Anchor start position"
        return self.overlay.anchor_points[0].start_circle.scenePos()

    def _get_ending_position(self) -> QPointF:
        # If the animation has an end position, use the Anchor end position
        return self.overlay.anchor_points[0].end_circle.scenePos()

    def _on_animation_finished(self, animation_ref):
        anim = animation_ref()
        if anim in self.active_animations:
            self.active_animations.remove(anim)
        # anim is scheduled to deleteLater, so after event loop returns control,
        # it should be cleaned up.

    def run_directional_animation_test(self):
        starting_pos = self._get_starting_position()
        ending_pos = self._get_ending_position()

        def start_next_animation(count=1):
            if count > 5:
                return

            anim_text = self._create_base_animation_text()
            self.overlay.addItem(anim_text)

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

            anim_ref = weakref.ref(anim)

            def finished():
                self._on_animation_finished(anim_ref)

            anim.finished.connect(finished)
            self.active_animations.append(anim)
            anim.start()

            QTimer.singleShot(250, lambda: start_next_animation(count + 1))

        start_next_animation()

    def run_parabola_animation_test(self):
        starting_pos = self._get_starting_position()
        ending_pos = self._get_ending_position()
        parabola_points = [
            AnimationPointF((starting_pos.x() + ending_pos.x()) / 2, starting_pos.y() - 100, 0.5),
        ]

        def start_next_animation(count=1):
            if count > 5:
                return

            anim_text = self._create_base_animation_text()
            self.overlay.addItem(anim_text)

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
                fade_in_easing_style=QEasingCurve.Type.OutQuad,
                fade_out_easing_style=QEasingCurve.Type.InQuad,
                animation_object=anim_text,
                ending_position=ending_pos,
                easing_style=QEasingCurve.Type.InOutQuad,
                parabola_points=parabola_points
            )

            anim_ref = weakref.ref(anim)

            def finished():
                self._on_animation_finished(anim_ref)

            anim.finished.connect(finished)
            self.active_animations.append(anim)
            anim.start()

            QTimer.singleShot(250, lambda: start_next_animation(count + 1))

        start_next_animation()

    def run_swivel_animation_test(self):
        starting_pos = QPointF(1280.0, 700.0)  # Manual start pos
        swivel_pos = QPointF(1920.0, 350.0)  # Manual swivel pos
        ending_pos = QPointF(2560.0, 350.0)  # Manual ending pos
        duration = 10000
        fade_in_duration = int(duration * 0.1)
        fade_out_duration = int(duration * 0.1)
        fade_out_delay = int(duration - fade_out_duration)
        phase_1_duration = int(duration / 2)
        phase_2_duration = int(duration / 2)
        playback_speed = int(duration * 0.23)

        def start_next_animation(count=1):
            if count > 5:
                QTimer.singleShot(duration + 3000, self.quit)
                return

            anim_text = self._create_base_animation_text()
            self.overlay.addItem(anim_text)

            anim = SwivelAnimation(
                animation_type="Swivel",
                sound=self._create_sound_effect(),
                duration=duration,
                starting_position=starting_pos,
                fade_in=True,
                fade_out=True,
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

            anim_ref = weakref.ref(anim)

            def finished():
                self._on_animation_finished(anim_ref)

            anim.finished.connect(finished)
            self.active_animations.append(anim)
            anim.start()

            QTimer.singleShot(playback_speed, lambda: start_next_animation(count + 1))

        start_next_animation()

    def run_pow_animation_test(self):
        starting_pos = self._get_starting_position()

        def start_next_animation(count=1):
            if count > 5:
                return

            anim_text = self._create_base_animation_text()
            self.overlay.addItem(anim_text)

            anim = PowAnimation(
                animation_type="Pow",
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
                jiggle=False,
                jiggle_intensity=100,
                scale_percentage=1.5,
                scale_easing_style=QEasingCurve.Type.OutBounce,
                phase_1_duration=500,
                phase_2_duration=500
            )

            anim_ref = weakref.ref(anim)

            def finished():
                self._on_animation_finished(anim_ref)

            anim.finished.connect(finished)
            self.active_animations.append(anim)
            anim.start()

            QTimer.singleShot(250, lambda: start_next_animation(count + 1))

        start_next_animation()

    def run_stationary_animation_test(self):
        starting_pos = self._get_starting_position()

        def start_next_animation(count=1):
            if count > 5:
                return

            anim_text = self._create_base_animation_text()
            self.overlay.addItem(anim_text)

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

            anim_ref = weakref.ref(anim)

            def finished():
                self._on_animation_finished(anim_ref)

            anim.finished.connect(finished)
            self.active_animations.append(anim)
            anim.start()

            QTimer.singleShot(250, lambda: start_next_animation(count + 1))

        start_next_animation()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    app = AnimationTester(sys.argv)
    # Instead of calling app.run_swivel_animation_test() directly, we start the event loop
    # and then trigger the test after a short delay, ensuring the main window and overlay are ready.

    # Uncomment the test you want to run:
    # QTimer.singleShot(0, app.run_directional_animation_test)
    # QTimer.singleShot(0, app.run_parabola_animation_test)
    QTimer.singleShot(0, app.run_swivel_animation_test)
    # QTimer.singleShot(0, app.run_pow_animation_test)
    # QTimer.singleShot(0, app.run_stationary_animation_test)

    app.run()  # Starts the event loop
