import threading
import time
from datetime import datetime
from pathlib import Path

import spm_control.core_config as core_config
from spm_control.gui.modes.page_helpers import throwError


def get_tttr_num(folder_path):
    most_recent = 0

    for path in folder_path.iterdir():
        if path.is_dir() and path.name.startswith("n"):
            number = path.name.split("_", 1)[0].removeprefix("n")

            if number.isdigit():
                most_recent = max(most_recent, int(number))

    return most_recent + 1

class TTTRManager:
    MODE_MAP = {"t2": 2, "t3": 3}

    def __init__(self, gui_root, hardware_manager, time_manager=None):
        self.gui_root = gui_root
        self.hardware_manager = hardware_manager
        self.time_manager = time_manager

        self.thread = None
        self.stop_event = threading.Event()

        self.active_file = None
        self.last_result = None
        self.error = None
        self.status = "idle"
        self.acquisition_ms = 0
        self.start_time = None

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def get_active_file(self):
        return self.active_file

    def get_status(self):
        return self.status

    def start(self, acquisition_ms):
        try:
            if self.is_running():
                raise RuntimeError("A TTTR measurement is already running.")

            acquisition_ms = int(acquisition_ms)

            if acquisition_ms <= 0:
                raise ValueError("Acquisition time must be greater than zero.")

            hydraharp_settings = core_config.load_named_settings("hydraharp", core_config.HARDWARE_CONFIG)
            scan_settings = core_config.load_named_settings("scan", core_config.SCAN_CONFIG)
            move_settings = core_config.load_named_settings("move", core_config.SCAN_CONFIG)

            mode = hydraharp_settings.get("default_mode", "hist").lower()

            x = float(move_settings["x"])
            y = float(move_settings["y"])
            acquisition_s = acquisition_ms / 1000

            today = datetime.today().strftime("%Y-%m-%d")
            tttr_root = Path(scan_settings["folder_path"]) / today / "tttr"
            tttr_root.mkdir(parents=True, exist_ok=True)

            measurement_number = get_tttr_num(tttr_root)
            acquisition_text = f"{acquisition_s:g}"
            folder_name = f"n{measurement_number}_{mode.upper()}_x{x:.3f}_y{y:.3f}_aq{acquisition_text}s"

            self.active_folder = tttr_root / folder_name

            if self.active_folder.exists():
                raise FileExistsError(f"TTTR folder already exists: {self.active_folder}")

            self.active_folder.mkdir()
            self.active_file = self.active_folder / "raw.out"
            self.active_position = {"x": x, "y": y}
            self.acquisition_ms = acquisition_ms

            self.stop_event.clear()
            self.last_result = None
            self.error = None
            self.status = "starting"
            self.start_time = None

            if self.time_manager is not None:
                self.time_manager.start(total_units=acquisition_ms)

            self.thread = threading.Thread(target=self._run, args=(mode,), daemon=True, name="TTTRWorker")
            self.thread.start()
            self.gui_root.after(100, self._update_time)

            return self.active_file

        except Exception as error:
            self.error = error
            self.status = "error"
            print(f"TTTR measurement failed: {error}")
            self.gui_root.after(0, throwError, str(error))

        finally:
            self.thread = None

    def _run(self, mode):
        try:
            self.status = "connecting"

            self.hardware_manager.close_detector()
            detector = self.hardware_manager.connect_detector()

            if detector is None:
                detector = self.hardware_manager.detector

            if detector is None or detector.manager is None:
                raise RuntimeError("HydraHarp detector failed to connect.")

            self.status = "running"
            self.start_time = time.monotonic()

            with self.hardware_manager.detector_lock:
                self.hardware_manager.set_operation("tttr")

                try:
                    if mode == "t2":
                        detector.manager.t2_meas(filename=str(self.active_file), tacq=self.acquisition_ms)
                    else:
                        raise NotImplementedError("T3 acquisition is not implemented yet.")
                finally:
                    self.hardware_manager.set_operation("idle")

            if self.stop_event.is_set():
                self.status = "stopped"
            else:
                self.last_result = {"mode": mode, "file": self.active_file, "acquisition_ms": self.acquisition_ms}
                self.status = "complete"

        except Exception as error:
            self.error = error
            self.status = "error"
            print(f"TTTR measurement failed: {error}")
            self.gui_root.after(0, throwError, str(error))

        finally:
            if self.time_manager is not None:
                self.gui_root.after(0, self.time_manager.finish)

            self.thread = None

    def _update_time(self):
        if not self.is_running():
            return

        if self.start_time is not None and self.time_manager is not None:
            elapsed_s = time.monotonic() - self.start_time
            remaining_s = max(0, self.acquisition_ms / 1000 - elapsed_s)
            self.time_manager.update_known_duration(remaining_s)

        self.gui_root.after(100, self._update_time)

    def stop(self):
        if not self.is_running():
            return

        self.stop_event.set()
        self.status = "stopping"