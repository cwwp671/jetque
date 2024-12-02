# jetque/jetque.py

from PyQt6.QtWidgets import QApplication
from jetque.source.gui.jetque_window import JetQueWindow
from jetque.source.gui.jetque_overlay import JetQueOverlay
from jetque.source.utilities.global_key_listener_thread import GlobalKeyListenerThread
import logging
import sys

NUMBER_OF_OVERLAYS: int = 3

class JetQue(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.window = JetQueWindow()
        self.overlays = [JetQueOverlay() for _ in range(NUMBER_OF_OVERLAYS)]
        self.some_attribute = True  # Example attribute

        # Initialize and start the global key listener thread
        self.key_listener_thread = GlobalKeyListenerThread()
        self.key_listener_thread.key_pressed.connect(self.handle_global_key_press)
        self.key_listener_thread.start()
        logging.debug("GlobalKeyListenerThread started.")

    def handle_global_key_press(self, key, modifiers):
        if key == 'f12':
            logging.debug("F12 Key Pressed.")

            for overlay in self.overlays:
                overlay.mode_switch()

    def run(self):
        exit_code = self.exec()
        logging.debug("Application exiting. Stopping GlobalKeyListenerThread.")
        self.key_listener_thread.stop()
        sys.exit(exit_code)
