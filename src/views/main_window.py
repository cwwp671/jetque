# jetque/src/views/main_window.py

import sys
import pdb
import traceback
import os
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, pyqtSlot
from pathlib import Path
from src.overlays.configure_overlay import ConfigureOverlay
from src.overlays.overlay_manager import OverlayManager
from src.views.system_tray import SystemTrayIcon
from src.views.home_view import HomeView
from src.views.overlays_view import OverlaysView
from src.views.triggers_view import TriggersView
from src.events.event_handler import EventHandler
from src.workers.chat_log_parser_worker import ChatLogParserWorker
from src.workers.dbg_log_parser_worker import DBGLogParserWorker
from src.events.event import Event
from config.debug_config import is_debug_mode


class MainWindow(QMainWindow):
    def __init__(self):
        logging.debug("Initializing MainWindow")
        super().__init__()
        self.setWindowTitle("JetQue")
        self.setGeometry(100, 100, 800, 600)

        # Initialize worker threads and workers to None
        self.chat_thread = None
        self.dbg_thread = None
        self.chat_worker = None
        self.dbg_worker = None

        self.is_running = False
        self.is_test_mode = False
        self.test_log_simulation_enabled = False
        self.saved_chat_log_file = None
        self.overlay_manager = OverlayManager()
        self.event_handler = EventHandler()

        self.setup_icon()
        self.setup_ui()
        self.setup_tray()
        self.event_handler.incoming_event_signal.connect(self.handle_incoming_event)
        self.event_handler.outgoing_event_signal.connect(self.handle_outgoing_event)
        self.setup_connections()
        print(f"Debug Mode: {os.getenv('JETQUE_DEBUG', 'False')}")

    def debug_breakpoint(self, condition=True):
        """
        Invoke pdb.set_trace() if the condition is True and in debug mode.
        """
        if is_debug_mode() and condition:
            logging.debug("Conditional breakpoint triggered")
            pdb.set_trace()

    def setup_icon(self):
        logging.debug("Setting up application icon")
        current_dir = Path(__file__).parent
        icon_path = current_dir / 'resources' / 'JetQue_Icon.png'

        if icon_path.exists():
            icon = QIcon(str(icon_path))
            self.setWindowIcon(icon)
        else:
            self.setWindowIcon(QIcon.fromTheme("application-icon"))

    def setup_ui(self):
        logging.debug("Setting up UI for MainWindow")
        # Setup Menu Bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        # Setup Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.home_view = HomeView()
        self.tabs.addTab(self.home_view, "Home")

        self.overlays_view = OverlaysView(self.overlay_manager)
        self.tabs.addTab(self.overlays_view, "Overlays")

        self.triggers_view = TriggersView()
        self.tabs.addTab(self.triggers_view, "Triggers")

        # Add Play/Stop button at the top-right corner
        self.play_stop_button = QPushButton()
        self.set_play_button_icon()  # Initially set as Play button
        self.play_stop_button.clicked.connect(self.toggle_run_state)

        self.test_button = QPushButton("Test")
        self.test_button.setCheckable(True)
        self.test_button.clicked.connect(self.toggle_test_mode)

        # Create a layout for the button at the top-right
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push button to the right
        button_layout.addWidget(self.play_stop_button)
        button_layout.addWidget(self.test_button)

        # Add the button layout above the tabs
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)  # Add button to top
        main_layout.addWidget(self.tabs)  # Tabs come below the button

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_play_button_icon(self):
        """Set the button icon to green play."""
        logging.debug("Setting play button icon")
        play_icon_path = Path(__file__).parent / 'resources' / 'play_icon.png'
        if play_icon_path.exists():
            play_icon = QIcon(str(play_icon_path))
        else:
            play_icon = QIcon.fromTheme("media-playback-start")
            logging.warning(f"Play icon not found at {play_icon_path}. Using default icon.")
        self.play_stop_button.setIcon(play_icon)
        self.play_stop_button.setStyleSheet("background-color: green; border-radius: 10px;")

    def set_stop_button_icon(self):
        """Set the button icon to red stop."""
        logging.debug("Setting stop button icon")
        stop_icon_path = Path(__file__).parent / 'resources' / 'stop_icon.png'
        if stop_icon_path.exists():
            stop_icon = QIcon(str(stop_icon_path))
        else:
            stop_icon = QIcon.fromTheme("media-playback-stop")
            logging.warning(f"Stop icon not found at {stop_icon_path}. Using default icon.")
        self.play_stop_button.setIcon(stop_icon)
        self.play_stop_button.setStyleSheet("background-color: red; border-radius: 10px;")

    def toggle_test_mode(self):
        """Toggles Test Mode on or off."""
        logging.debug("Toggling test mode")
        if self.test_button.isChecked():
            self.is_test_mode = True
            self.activate_test_mode()
        else:
            self.is_test_mode = False
            self.deactivate_test_mode()

    def activate_test_mode(self):
        """Activates Test Mode by setting appropriate states."""
        logging.debug("Activating test mode")

        # 1. Save the current chat log file
        self.saved_chat_log_file = self.home_view.config_data.get('char_file', '')
        logging.debug(f"Saved Log: {self.saved_chat_log_file}")

        # 2. Set dummy log file for testing
        dummy_chat_log = 'C:/Everquest/Logs/dummy_chat_log.txt'
        self.home_view.config_data['char_file'] = dummy_chat_log
        logging.debug(f"Switching Active Chat Log to: {self.home_view.config_data['char_file']}")

        # 3. Switch overlays to active mode
        for overlay_name in list(self.overlay_manager.overlays.keys()):
            current_overlay = self.overlay_manager.overlays[overlay_name]
            if isinstance(current_overlay, ConfigureOverlay):  # Only if in config mode
                logging.debug(f"{current_overlay.name} in Config Mode. Switching to Active Mode")
                self.overlay_manager.toggle_mode(overlay_name)

        # 4. Stop DBGLogParserWorker if running
        if hasattr(self, 'dbg_thread') and self.dbg_thread is not None:
            if self.dbg_thread.isRunning():
                logging.debug("Stopping DBG Log Parser Worker before entering Test Mode")
                self.dbg_worker.stop_monitoring()
                self.dbg_thread.quit()
                self.dbg_thread.wait()
                self.dbg_worker = None
                self.dbg_thread = None
                logging.debug("DBG Log Parser Worker stopped")
            else:
                logging.debug("DBG Log Parser Worker exists but is not running.")
        else:
            logging.debug("DBG Log Parser Worker does not exist. No need to stop.")

        # 5. Set play/stop button to Stop mode
        if not self.is_running:
            logging.debug("Play Button switching to Stop")
            self.is_running = True
            self.set_stop_button_icon()
            self.start_parsing(test_mode=True)

    def deactivate_test_mode(self):
        """Deactivates Test Mode by resetting states."""
        logging.debug("Deactivating test mode")

        # 1. Restore the saved chat log file
        if self.saved_chat_log_file:
            self.home_view.config_data['char_file'] = self.saved_chat_log_file
            logging.debug(f"Switching Active Chat Log to {self.home_view.config_data['char_file']}")

            # Stop ChatLogParserWorker
        if self.chat_worker and self.chat_thread and self.chat_thread.isRunning():
            self.chat_worker.stop_parsing()
            self.chat_thread.quit()
            self.chat_thread.wait()
            self.chat_worker = None
            self.chat_thread = None
            logging.debug("Chat Log Parser thread stopped")
        else:
            logging.debug("Chat Log Parser thread is not running or already stopped.")

        # Stop DBGLogParserWorker
        if hasattr(self, 'dbg_worker') and self.dbg_worker and self.dbg_thread and self.dbg_thread.isRunning():
            self.dbg_worker.stop_monitoring()
            self.dbg_thread.quit()
            self.dbg_thread.wait()
            self.dbg_worker = None
            self.dbg_thread = None
            logging.debug("DBG Log Parser thread stopped")
        else:
            logging.debug("DBG Log Parser thread is not running or already stopped")

        # 4. Set play/stop button to Play mode if not running
        if self.is_running:
            logging.debug("Stop Button switching to Play")
            self.is_running = False
            self.set_play_button_icon()

    def toggle_run_state(self):
        """Toggles the program's running state and updates the button."""
        logging.debug("Toggling run state")
        if self.is_running:
            self.is_running = False
            self.set_play_button_icon()
            self.stop_all_threads()
            # Optional: Conditional breakpoint when stopping
            self.debug_breakpoint(condition=False)  # Adjust condition as needed
        else:
            self.is_running = True
            self.set_stop_button_icon()
            self.start_parsing()
            # Optional: Conditional breakpoint when starting
            self.debug_breakpoint(condition=False)  # Adjust condition as needed

    def start_parsing(self, test_mode=False):
        """Start the log parsing with an option for test mode."""
        logging.debug("Starting parsing threads")
        chat_log_file = self.home_view.config_data.get('char_file', '')
        dbg_log_file = self.home_view.config_data.get('dbg_file', '')

        if not chat_log_file:
            logging.error("Chat log file path is not set properly. Please check your configuration.")
            QMessageBox.critical(self, "Configuration Error", "Chat log file path is not set properly. Please check your configuration.")
            return

        # Prevent multiple ChatLogParserWorker instances
        if self.chat_worker and self.chat_thread and self.chat_thread.isRunning():
            logging.debug("ChatLogParserWorker is already running. Skipping restart.")
        else:
            # Setup Chat Log Parser Worker
            self.chat_thread = QThread()
            self.chat_worker = ChatLogParserWorker(chat_log_file, self.event_handler, test_mode)
            self.chat_worker.moveToThread(self.chat_thread)
            self.chat_thread.started.connect(self.chat_worker.start_parsing)
            self.chat_worker.new_event_signal.connect(self.handle_new_chat_event)
            self.chat_worker.error_signal.connect(self.handle_worker_error)
            self.chat_worker.finished.connect(self.chat_thread.quit)
            self.chat_worker.finished.connect(self.chat_worker.deleteLater)
            self.chat_thread.finished.connect(self.chat_thread.deleteLater)
            self.chat_thread.start()
            logging.debug("Chat Log Parser thread started")

        if not test_mode:
            if not dbg_log_file:
                logging.error("DBG log file path is not set properly. Please check your configuration.")
                QMessageBox.critical(self, "Configuration Error", "DBG log file path is not set properly. Please check your configuration.")
                return

            # Prevent multiple DBGLogParserWorker instances
            if hasattr(self, 'dbg_worker') and self.dbg_worker and self.dbg_thread and self.dbg_thread.isRunning():
                logging.debug("DBGLogParserWorker is already running. Skipping restart.")
            else:
                # Setup DBG Log Parser Worker
                self.dbg_thread = QThread()
                self.dbg_worker = DBGLogParserWorker(dbg_log_file)
                self.dbg_worker.moveToThread(self.dbg_thread)
                self.dbg_thread.started.connect(self.dbg_worker.start_monitoring)
                self.dbg_worker.dbg_info_signal.connect(self.handle_new_dbg_event)
                self.dbg_worker.error_signal.connect(self.handle_worker_error)
                self.dbg_worker.finished.connect(self.dbg_thread.quit)
                self.dbg_worker.finished.connect(self.dbg_worker.deleteLater)
                self.dbg_thread.finished.connect(self.dbg_thread.deleteLater)
                self.dbg_thread.start()
                logging.debug("DBG Log Parser thread started")

    @pyqtSlot(Event)
    def handle_incoming_event(self, event):
        logging.debug(f"Handling incoming event: {event}")
        self.overlay_manager.display_event('Incoming', event)

    @pyqtSlot(Event)
    def handle_outgoing_event(self, event):
        logging.debug(f"Handling outgoing event: {event}")
        self.overlay_manager.display_event('Outgoing', event)

    @pyqtSlot(str)
    def handle_new_chat_event(self, event: str):
        """Handle a new chat log event."""
        logging.debug(f"New chat event detected: {event}")
        print(f"New chat event detected: {event}")
        # Example condition: Breakpoint when a specific keyword is in the event
        if "critical_error" in event:
            self.debug_breakpoint(condition=True)

    @pyqtSlot(str)
    def handle_new_dbg_event(self, info: str):
        """Handle new dbg information."""
        logging.debug(f"New dbg info detected: {info}")
        print(f"New dbg info detected: {info}")
        # Example condition: Breakpoint on specific dbg info
        if "server_failure" in info:
            self.debug_breakpoint(condition=True)

    def setup_tray(self):
        logging.debug("Setting up system tray")
        self.tray_icon = SystemTrayIcon(self)
        self.tray_icon.show()

    def setup_connections(self):
        logging.debug("Setting up signal-slot connections")
        self.tray_icon.show_requested.connect(self.restore_window)

    def restore_window(self):
        logging.debug("Restoring main window from system tray")
        self.showNormal()
        self.show()
        self.raise_()
        self.activateWindow()

    def stop_all_threads(self):
        """Gracefully stop all running threads."""
        logging.debug("Stopping all threads")

        # Stop ChatLogParserWorker
        if self.chat_worker and self.chat_thread and self.chat_thread.isRunning():
            self.chat_worker.stop_parsing()
            self.chat_thread.quit()
            self.chat_thread.wait()
            self.chat_worker = None
            self.chat_thread = None
            logging.debug("Chat Log Parser thread stopped")
        else:
            logging.debug("Chat Log Parser thread is not running or already stopped.")

        # Stop DBGLogParserWorker
        if hasattr(self, 'dbg_worker') and self.dbg_worker and self.dbg_thread and self.dbg_thread.isRunning():
            self.dbg_worker.stop_monitoring()
            self.dbg_thread.quit()
            self.dbg_thread.wait()
            self.dbg_worker = None
            self.dbg_thread = None
            logging.debug("DBG Log Parser thread stopped")
        else:
            logging.debug("DBG Log Parser thread is not running or already stopped")

    def handle_worker_error(self, error_message):
        """Handle errors emitted from workers."""
        logging.error(f"Worker Error: {error_message}")
        QMessageBox.critical(self, "Worker Error", f"An error occurred: {error_message}")
        self.stop_all_threads()
        self.set_play_button_icon()
        self.is_running = False
        # Optional: Breakpoint on worker error
        self.debug_breakpoint(condition=is_debug_mode())

    def closeEvent(self, event):
        logging.debug("MainWindow: Close event triggered")
        self.stop_all_threads()
        event.accept()


# Entry point for the application
def excepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    # Only activate pdb.post_mortem if in debug mode and traceback is valid
    if is_debug_mode() and exc_traceback:
        try:
            pdb.post_mortem(exc_traceback)
        except UnicodeDecodeError as ude:
            logging.error(f"UnicodeDecodeError during post-mortem debugging: {ude}")
            QMessageBox.critical(None, "Fatal Error", f"An unexpected error occurred: {exc_value}")
    else:
        QMessageBox.critical(None, "Fatal Error", f"An unexpected error occurred: {exc_value}")


def run_app():

    # Set the global exception hook
    sys.excepthook = excepthook

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

    logging.debug("Starting application")
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
