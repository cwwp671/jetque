# jetque/source/animations/animation_anchor.py

from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsObject
from PyQt6.QtCore import QRectF, pyqtSignal

from jetque.source.animations.animation_anchor_circle import AnimationAnchorCircle
from jetque.source.animations.animation_anchor_text import AnimationAnchorText


class AnimationAnchor(QGraphicsObject):
    positionChanged = pyqtSignal()

    def __init__(self, group_name, parent=None):
        super().__init__(parent)
        self.group_name = group_name

        # Start point
        self.start_circle = AnimationAnchorCircle()
        self.start_circle.setParentItem(self)
        self.start_circle.setPos(0, 0)

        self.start_text = AnimationAnchorText(
            group_name,
            is_start=True,
            parent=self.start_circle
        )
        self.start_text.setPos(0, -30)  # Position above the circle

        # End point
        self.end_circle = AnimationAnchorCircle()
        self.end_circle.setParentItem(self)
        self.end_circle.setPos(200, 0)

        self.end_text = AnimationAnchorText(
            group_name,
            is_start=False,
            parent=self.end_circle
        )
        self.end_text.setPos(0, -30)  # Position above the circle

        # Connect signals
        self.start_circle.positionChanged.connect(self.start_text.update_position)
        self.end_circle.positionChanged.connect(self.end_text.update_position)

        # Connect child signals to emit positionChanged
        self.start_circle.positionChanged.connect(self.on_child_changed)
        self.end_circle.positionChanged.connect(self.on_child_changed)
        self.start_text.contentChanged.connect(self.on_child_changed)
        self.end_text.contentChanged.connect(self.on_child_changed)

    def paint(self, painter: QPainter, option, widget=None):
        # No painting required; child items handle their own painting
        pass

    def on_child_changed(self):
        self.positionChanged.emit()

    def boundingRect(self) -> QRectF:
        # Calculate the bounding rectangle that contains both circles and texts
        start_rect = self.start_circle.mapToParent(self.start_circle.boundingRect()).boundingRect()
        end_rect = self.end_circle.mapToParent(self.end_circle.boundingRect()).boundingRect()
        return start_rect.united(end_rect)
