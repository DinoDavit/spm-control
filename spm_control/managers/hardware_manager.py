import threading

import spm_control.config as config
from spm_control.hardware.hydraharp import HydraHarpDetector


class HardwareManager:
    def __init__(self):
        self.detector = None
        self.detector_lock = threading.Lock()
        self.connection_lock = threading.Lock()

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

    def close_detector(self):
        with self.connection_lock:
            with self.detector_lock:
                if self.detector is not None:
                    self.detector.close()
                    self.detector = None