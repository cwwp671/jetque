# jetque/jetque.py

import logging
import sys

from PyQt6.QtWidgets import QApplication

from jetque.source.animations.animation_anchor import AnimationAnchor
from jetque.source.gui.jetque_window import JetQueWindow
from jetque.source.gui.jetque_overlay import JetQueOverlay
from jetque.source.utilities.global_key_listener_thread import GlobalKeyListenerThread


class JetQue(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        screen = QApplication.primaryScreen()
        available_geometry = screen.availableGeometry()

        self.window = JetQueWindow()
        self.overlay = JetQueOverlay(available_geometry)
        test_anchor = AnimationAnchor("Incoming")
        self.overlay.add_anchor_point(test_anchor)

        # Initialize and start the global key listener thread
        self.key_listener_thread = GlobalKeyListenerThread()
        self.key_listener_thread.key_pressed.connect(self.handle_global_key_press)
        self.key_listener_thread.start()
        logging.debug("GlobalKeyListenerThread started.")

    def handle_global_key_press(self, key, modifiers):
        if key == 'f12':
            logging.debug("F12 Key Pressed.")
            self.overlay.switch_mode()

    def run(self):
        exit_code = self.exec()
        logging.debug("Application exiting. Stopping GlobalKeyListenerThread.")
        self.key_listener_thread.stop()
        sys.exit(exit_code)
