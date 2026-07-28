import threading
from datetime import datetime
from pathlib import Path

import spm_control.config as config
#from spm_control.scan.TTTR_queue import TTTRQueue


class TTTRManager:
    MODE_MAP = {"T2": 2, "T3": 3}

    def __init__(self, gui_root, hardware_manager, time_manager=None):
        self.gui_root = gui_root
        self.hardware_manager = hardware_manager
        self.time_manager = time_manager

        self.thread = None
        self.stop_event = threading.Event()

        self.active_file = None
        self.active_position = None
        self.last_result = None
        self.error = None
        self.status = "idle"

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def get_active_file(self):
        return self.active_file

    def get_status(self):
        return self.status