import threading

import spm_control.config as config
from spm_control.hardware.hydraharp import HydraHarpDetector


class HardwareManager:
    def __init__(self):
        self.detector = None

        self.detector_lock = threading.Lock()
        self.connection_lock = threading.Lock()
        self.state_lock = threading.Lock()

        self.current_operation = "idle"
        self.latest_counts = (0, 0)

    def connect_detector(self):
        with self.connection_lock:
            if self.detector is not None:
                return self.detector

            hydraharp_settings = config.load_named_settings("hydraharp", config.HARDWARE_CONFIG)
            sync_settings = config.load_named_settings("sync", config.HARDWARE_CONFIG)

            detector = HydraHarpDetector(hydraharp_settings, sync_settings)
            detector.connect()
            self.detector = detector

            return self.detector

    def set_operation(self, operation):
        with self.state_lock:
            self.current_operation = operation

    def get_operation(self):
        with self.state_lock:
            return self.current_operation

    def set_latest_counts(self, ch1, ch2):
        with self.state_lock:
            self.latest_counts = (ch1, ch2)

    def get_latest_counts(self):
        with self.state_lock:
            return self.latest_counts
    # Getter and constructor methods for live count display

    def close_detector(self):
        with self.connection_lock:
            with self.detector_lock:
                if self.detector is not None:
                    self.detector.close()
                    self.detector = None

                with self.state_lock:
                    self.current_operation = "idle"
                    self.latest_counts = (0, 0)