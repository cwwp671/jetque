# jetque/source/gui/jetque_overlay.py

import logging

from PyQt6.QtWidgets import QGraphicsScene

from jetque.source.gui.jetque_view import JetQueView


class JetQueOverlay(QGraphicsScene):
    def __init__(self, geometry, parent=None):
        super().__init__(parent)
        logging.debug("JetQueOverlay: Initializing.")
        self.view: JetQueView = JetQueView(self, geometry)
        self.is_configuration_mode: bool = False
        self.anchor_points = []

    def add_anchor_point(self, anchor_point):
        self.addItem(anchor_point)
        self.anchor_points.append(anchor_point)
        anchor_point.positionChanged.connect(self.view.update_mask)

    def switch_mode(self):
        logging.debug("Switching modes.")

        if self.is_configuration_mode:
            self.run_mode()
        else:
            self.configuration_mode()

    def run_mode(self):
        logging.debug("Configuration mode off.")
        self.is_configuration_mode = False
        self.view.run_mode()

    def configuration_mode(self):
        logging.debug("Configuration mode on.")
        self.is_configuration_mode = True
        self.view.configuration_mode()
