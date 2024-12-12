import logging
import sys
from PyQt6.QtCore import Qt, QPointF, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, \
    QAbstractAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPen, QPainter
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView

from jetque.source.gui.items.jq_graphics_pixmap_item import JQGraphicsPixmapItem
from jetque.source.gui.items.jq_graphics_text_item import JQGraphicsTextItem
from jetque.source.gui.items.jq_graphics_simple_text_item import JQGraphicsSimpleTextItem


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    app = QApplication(sys.argv)

    # Create a QGraphicsScene
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 1920, 1080)

    font_size = 12
    test_outline = True
    test_drop_shadow = True

    pen_test = QPen(Qt.GlobalColor.white, 1.0)
    pen_test.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen_test.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

    # Create a custom text item
    simple_text_item = JQGraphicsSimpleTextItem(
        font=QFont("Helvetica", font_size, QFont.Weight.Bold),
        text="Simple Text",
        color=QColor(Qt.GlobalColor.black),
        outline=test_outline,
        outline_pen=pen_test,
        drop_shadow=test_drop_shadow,
        drop_shadow_offset=QPointF(3.5, 6.1),
        drop_shadow_blur_radius=7.0,
        drop_shadow_color=QColor(0, 0, 0, 191)
    )

    rich_text_item = JQGraphicsTextItem(
        font=QFont("Helvetica", font_size, QFont.Weight.Bold),
        text="Rich Text",
        color=QColor(Qt.GlobalColor.black),
        outline=test_outline,
        outline_pen=pen_test,
        drop_shadow=test_drop_shadow,
        drop_shadow_offset=QPointF(3.5, 6.1),
        drop_shadow_blur_radius=7.0,
        drop_shadow_color=QColor(0, 0, 0, 191)
    )

    pixmap_pen = QPen(Qt.GlobalColor.red, 4)
    pixmap_pen.setStyle(Qt.PenStyle.SolidLine)
    pixmap_pen.setCapStyle(Qt.PenCapStyle.SquareCap)
    pixmap_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)

    pixmap_item = JQGraphicsPixmapItem(
        file_path="C:/intellij-projects/jetque/jetque/resources/default.png",
        outline=True,
        outline_pen=pixmap_pen,
        drop_shadow=test_drop_shadow,
        drop_shadow_offset=QPointF(3.5, 6.1),
        drop_shadow_blur_radius=7.0,
        drop_shadow_color=QColor(0, 0, 0, 191)
    )

    pixmap_item.setParentItem(rich_text_item)

    # Create a QGraphicsView
    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.RenderHint.Antialiasing)
    view.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    view.setBackgroundBrush(Qt.GlobalColor.darkGray)
    view.setWindowTitle("PyQt6 Graphics View Example")
    view.resize(1920, 1080)
    view.show()

    # scene.addItem(simple_text_item)
    scene.addItem(rich_text_item)
    # scene.addItem(pixmap_item)

    duration = 3000
    animation_group: QParallelAnimationGroup = QParallelAnimationGroup()
    starting_position = QPointF(
        (scene.width() / 2.0) - (rich_text_item.collision_rect.width() / 2.0),
        (scene.height() / 2.0) - (rich_text_item.collision_rect.height() / 2.0)
    )

    middle_position = QPointF(
        ((scene.width() / 2.0) + (scene.width() / 4.0))
        - (rich_text_item.collision_rect.width() / 2.0),
        ((scene.height() / 2.0) - (scene.height() / 4.0))
        - (rich_text_item.collision_rect.height() / 2.0)
    )

    ending_position = QPointF(
        scene.width() - (rich_text_item.collision_rect.width() / 2.0),
        ((scene.height() / 2.0) - (scene.height() / 4.0))
        - (rich_text_item.collision_rect.height() / 2.0)
    )

    animation: QPropertyAnimation = QPropertyAnimation(rich_text_item, b"pos")
    animation.setDuration(duration)
    animation.setStartValue(starting_position)
    animation.setKeyValueAt(0.5, middle_position)
    animation.setEndValue(ending_position)
    animation_group.addAnimation(animation)

    fade_in_animation: QPropertyAnimation = QPropertyAnimation(rich_text_item, b"opacity")
    fade_in_animation.setDuration(int(duration * 0.1))
    fade_in_animation.setStartValue(0.0)
    fade_in_animation.setEndValue(1.0)
    fade_in_animation.setEasingCurve(QEasingCurve.Type.Linear)
    animation_group.addAnimation(fade_in_animation)

    # Optional Fade-Out effect

    fade_out_animation: QPropertyAnimation = QPropertyAnimation(rich_text_item, b"opacity")
    fade_out_group: QSequentialAnimationGroup = QSequentialAnimationGroup()
    fade_out_animation.setDuration(int(duration * 0.1))
    fade_out_animation.setStartValue(1.0)
    fade_out_animation.setEndValue(0.0)
    fade_out_animation.setEasingCurve(QEasingCurve.Type.Linear)
    fade_out_group.addPause(int(duration - (duration * 0.1)))
    fade_out_group.addAnimation(fade_out_animation)
    animation_group.addAnimation(fade_out_group)

    animation_group.start(policy=QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
