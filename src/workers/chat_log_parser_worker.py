# jetque/src/workers/chat_log_parser_worker.py

import logging
import pdb
import sys
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
from src.parsers.chat_log_parser import ChatLogParser
from src.events.event_factory import EventFactory
from src.events.event_handler import EventHandler
from config.debug_config import is_debug_mode


class ChatLogParserWorker(QObject):
    new_event_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, log_file_path, event_handler: EventHandler, test_mode=False):
        super().__init__()
        self.log_file_path = log_file_path
        self.event_handler = event_handler
        self.test_mode = test_mode
        self.is_running = False
        self.chat_log_parser = None
        self.test_timers = []

    @pyqtSlot()
    def start_parsing(self):
        """Start the parsing process."""
        logging.debug("ChatLogParserWorker: Starting parsing")
        try:
            self.is_running = True
            self.chat_log_parser = ChatLogParser(self.log_file_path, self.event_handler, EventFactory())
            self.chat_log_parser.monitor_log()

            if self.test_mode:
                self.simulate_test_log()
        except Exception as e:
            logging.error(f"ChatLogParserWorker encountered an error: {e}")
            self.error_signal.emit(str(e))
            # Post-mortem debugging
            if is_debug_mode():
                _, _, tb = sys.exc_info()
                pdb.post_mortem(tb)
            self.finished.emit()

    def simulate_test_log(self):
        """Simulate log events using non-blocking timers."""
        logging.debug("ChatLogParserWorker: Starting test log simulation")

        # Timer for every 0.25 seconds
        timer_0_25 = QTimer()
        timer_0_25.timeout.connect(self.write_log_0_25)
        timer_0_25.start(250)

        # Timer for every 0.5 seconds
        timer_0_5 = QTimer()
        timer_0_5.timeout.connect(self.write_log_0_5)
        timer_0_5.start(500)

        # Timer for every 0.75 seconds
        timer_0_75 = QTimer()
        timer_0_75.timeout.connect(self.write_log_0_75)
        timer_0_75.start(750)

        # Store the timers to stop them later
        self.test_timers.extend([timer_0_25, timer_0_5, timer_0_75])

    def write_log_0_25(self):
        """Simulate log writing every 0.25 seconds."""
        try:
            with open(self.log_file_path, 'a') as dummy_log:
                dummy_log.write("A scary monster hits YOU for 100 points of damage.\n")
                dummy_log.write("You punch a scary monster for 100 points of damage.\n")
                dummy_log.flush()
            logging.debug("ChatLogParserWorker: Wrote simulated 0.25s log")
        except Exception as e:
            logging.error(f"Error writing simulated 0.25s log: {e}")
            self.error_signal.emit(str(e))
            if is_debug_mode():
                _, _, tb = sys.exc_info()
                pdb.post_mortem(tb)

    def write_log_0_5(self):
        """Simulate log writing every 0.5 seconds."""
        try:
            with open(self.log_file_path, 'a') as dummy_log:
                dummy_log.write("A scary monster tries to hit YOU, but misses!\n")
                dummy_log.write("You try to punch a scary monster, but miss!\n")
                dummy_log.flush()
            logging.debug("ChatLogParserWorker: Wrote simulated 0.5s log")
        except Exception as e:
            logging.error(f"Error writing simulated 0.5s log: {e}")
            self.error_signal.emit(str(e))
            if is_debug_mode():
                _, _, tb = sys.exc_info()
                pdb.post_mortem(tb)

    def write_log_0_75(self):
        """Simulate log writing every 0.75 seconds."""
        try:
            with open(self.log_file_path, 'a') as dummy_log:
                dummy_log.write("You backstab a scary monster for 100 points of damage.\n")
                dummy_log.write("A scary monster bashes you for 100 points of damage.\n")
                dummy_log.flush()
            logging.debug("ChatLogParserWorker: Wrote simulated 0.75s log")
        except Exception as e:
            logging.error(f"Error writing simulated 0.75s log: {e}")
            self.error_signal.emit(str(e))
            if is_debug_mode():
                _, _, tb = sys.exc_info()
                pdb.post_mortem(tb)

    @pyqtSlot()
    def stop_parsing(self):
        """Gracefully stop the parser and any test log simulation."""
        logging.debug("ChatLogParserWorker: Stopping parsing")
        self.is_running = False
        if self.chat_log_parser:
            self.chat_log_parser.stop_monitoring()

        # Stop all test mode timers if they exist
        for timer in self.test_timers:
            timer.stop()

        self.test_timers.clear()
        self.finished.emit()
