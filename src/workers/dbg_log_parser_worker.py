# jetque/src/workers/dbg_log_parser_worker.py

import logging
import pdb
import sys
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from src.parsers.dbg_log_parser import DBGLogParser
from config.debug_config import is_debug_mode


class DBGLogParserWorker(QObject):
    dbg_info_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, log_file_path):
        super().__init__()
        self.log_file_path = log_file_path
        self.is_running = False
        self.dbg_log_parser = None

    @pyqtSlot()
    def start_monitoring(self):
        """Start monitoring the DBG log."""
        logging.debug("DBGLogParserWorker: Starting DBG log monitoring")
        try:
            self.is_running = True
            self.dbg_log_parser = DBGLogParser(self.log_file_path)
            self.dbg_log_parser.monitor_log()

            # Connect DBGLogParser's signals to this worker's signals
            self.dbg_log_parser.info_signal.connect(self.dbg_info_signal.emit)
            self.dbg_log_parser.error_signal.connect(self.handle_parser_error)
        except Exception as e:
            logging.error(f"DBGLogParserWorker encountered an error: {e}")
            self.error_signal.emit(str(e))
            # Post-mortem debugging
            if is_debug_mode():
                _, _, tb = sys.exc_info()
                pdb.post_mortem(tb)
            self.finished.emit()

    @pyqtSlot()
    def stop_monitoring(self):
        """Gracefully stop the DBG log monitoring."""
        logging.debug("DBGLogParserWorker: Stopping DBG log monitoring")
        self.is_running = False
        if self.dbg_log_parser:
            self.dbg_log_parser.stop_monitoring()
        self.finished.emit()

    @pyqtSlot(str)
    def handle_parser_error(self, error_message):
        """Handle errors emitted from DBGLogParser."""
        logging.error(f"DBGLogParser Error: {error_message}")
        self.error_signal.emit(error_message)
        # Post-mortem debugging
        if is_debug_mode():
            _, _, tb = sys.exc_info()
            pdb.post_mortem(tb)
        self.stop_monitoring()
