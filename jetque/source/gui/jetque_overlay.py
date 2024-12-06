# jetque/source/gui/jetque_overlay.py

import logging
from typing import List, Optional

from PyQt6.QtCore import QObject, QRect, Qt
from PyQt6.QtWidgets import QGraphicsScene

from jetque.source.animations.anchor_object import AnchorObject
from jetque.source.gui.jetque_view import JetQueView


class JetQueOverlay(QGraphicsScene):
    """Overlay scene for JetQue, managing anchor points and configuration modes."""

    def __init__(self, geometry: QRect, parent: Optional[QObject] = None) -> None:
        """Initialize the overlay scene.

        Args:
            geometry (QRect): The available screen geometry.
            parent (Optional[QObject], optional): Parent object. Defaults to None.
        """
        super().__init__(parent)
        logging.debug("JetQueOverlay: Initializing.")
        self.view: JetQueView = JetQueView(self, geometry)
        self.is_configuration_mode: bool = False
        self.anchor_points: List[AnchorObject] = []

    def add_anchor_point(self, anchor_point: AnchorObject) -> None:
        """Add an anchor point to the scene.

        Args:
            anchor_point (AnchorObject): The anchor point to add.
        """
        self.addItem(anchor_point)
        anchor_point.hide()
        self.anchor_points.append(anchor_point)
        anchor_point.positionChanged.connect(self.view.update_mask)

    def configuration_mode(self) -> None:
        """Switch the overlay to configuration mode."""
        logging.debug("Configuration mode on.")
        self.is_configuration_mode = True

        for anchor_point in self.anchor_points:
            anchor_point.show()

        self.view.configuration_mode()

    def run_mode(self) -> None:
        """Switch the overlay to run mode."""
        logging.debug("Configuration mode off.")
        self.is_configuration_mode = False

        for anchor_point in self.anchor_points:
            anchor_point.hide()

        self.view.run_mode()

    def switch_mode(self) -> None:
        """Toggle between run mode and configuration mode."""
        logging.debug("Switching modes.")
        if self.is_configuration_mode:
            self.run_mode()
        else:
            self.configuration_mode()
