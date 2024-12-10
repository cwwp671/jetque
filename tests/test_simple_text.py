import logging
import sys
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QFont, QColor, QPen, QPainter
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView

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

    font_size = 36
    test_outline = True
    test_drop_shadow = False

    pen_test = QPen(Qt.GlobalColor.white, 2.0)
    pen_test.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen_test.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

    # Create a custom text item
    text_item = JQGraphicsSimpleTextItem(
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

    # Center the text item in the scene
    text_item.setPos((scene.width() - text_item.boundingRect().width()) / 2,
                     (scene.height() - text_item.boundingRect().height()) / 2)

    # Center the text item in the scene
    rich_text_item.setPos((scene.width() - rich_text_item.boundingRect().width()) / 2,
                          ((scene.height() - rich_text_item.boundingRect().height()) / 2) - 100
                          )

    # Create a QGraphicsView
    view = QGraphicsView(scene)
    view.setRenderHint(QPainter.RenderHint.Antialiasing)
    view.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    view.setBackgroundBrush(Qt.GlobalColor.darkGray)
    view.setWindowTitle("PyQt6 Graphics View Example")
    view.resize(1920, 1080)
    view.show()

    scene.addItem(text_item)
    scene.addItem(rich_text_item)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
