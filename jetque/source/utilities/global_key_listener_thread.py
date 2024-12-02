# jetque/source/utilities/global_key_listener_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
from pynput import keyboard
import logging

class GlobalKeyListenerThread(QThread):
    key_pressed = pyqtSignal(str, set)  # Signal with key and modifiers

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_modifiers = set()
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                key_char = key.char.lower()
            else:
                key_char = key.name.lower()  # For special keys
        except AttributeError:
            key_char = str(key).lower()

        # Update modifier keys
        if key in {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r}:
            self.current_modifiers.add('Shift')
        elif key in {keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}:
            self.current_modifiers.add('Ctrl')
        elif key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
            self.current_modifiers.add('Alt')
        elif key in {keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r}:
            self.current_modifiers.add('Cmd')

        self.logger.debug(f"Key pressed: {key_char}, Modifiers: {self.current_modifiers}")
        self.key_pressed.emit(key_char, self.current_modifiers.copy())

    def on_release(self, key):
        # Update modifier keys
        if key in {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r}:
            self.current_modifiers.discard('Shift')
        elif key in {keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}:
            self.current_modifiers.discard('Ctrl')
        elif key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
            self.current_modifiers.discard('Alt')
        elif key in {keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r}:
            self.current_modifiers.discard('Cmd')

    def run(self):
        self.listener.start()
        self.listener.join()

    def stop(self):
        self.listener.stop()
        self.quit()
        self.wait()
