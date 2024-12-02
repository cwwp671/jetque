# jetque/source/gui/jetque_overlay.py
import logging

from PyQt6.QtWidgets import QGraphicsScene

from jetque.source.gui.jetque_view import JetQueView


class JetQueOverlay(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        logging.debug("JetQueOverlay: Initializing.")
        self.view: JetQueView = JetQueView(self)

    def mode_switch(self):
        if self.view.is_active:
            logging.debug("JetQueOverlay: View is in Active Mode. Switching to Configuration Mode.")
            self.configuration_on()
            logging.debug("JetQueOverlay: Switched to Configuration Mode.")
        else:
            logging.debug("JetQueOverlay: View is in Configuration Mode. Switching to Active Mode.")
            self.active_on()
            logging.debug("JetQueOverlay: Switched to Active Mode.")

    def configuration_on(self):
        self.view.view_configuration_on()

    def active_on(self):
        self.view.view_active_on()
