import numpy as np

from spm_control.hardware.interfaces import DetectorInterface
from spm_control.work_in_progress_legacy_scripts.hydraharp_intensities import (
    HH400_Histo_Manager,
)


class HydraHarpDetector(DetectorInterface):
    def __init__(
        self,
        mode: int = 0,
        send_error_email: bool = False
    ):
        self.mode = mode
        self.send_error_email = send_error_email
        self.manager = None

    def connect(self) -> None:
        if self.manager is not None:
            return

        manager = HH400_Histo_Manager(
            mode=self.mode,
            send_error_email=self.send_error_email
        )

        try:
            manager.connect_device()
            manager.prep_measurements()
            self.manager = manager

        except Exception:
            manager.closeDevices()
            raise

    def poll_counts(self) -> np.ndarray:
        self._require_connection()
        return self.manager.poll_intensity()

    def integrate_counts(self, acquisition_ms: int) -> np.ndarray:
        self._require_connection()

        return self.manager.integrate_intensity(
            tacq=acquisition_ms
        )

    def run_t2(self, file_path: str, acquisition_ms: int) -> None:
        self._require_connection()

        self.manager.t2_meas(
            filename=file_path,
            tacq=acquisition_ms
        )

    def close(self) -> None:
        if self.manager is not None:
            self.manager.closeDevices()
            self.manager = None

    def _require_connection(self) -> None:
        if self.manager is None:
            raise RuntimeError("HydraHarp is not connected.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()