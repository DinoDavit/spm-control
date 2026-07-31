import threading
import time
import subprocess
from datetime import datetime
from pathlib import Path

import spm_control.core_config as core_config
from spm_control.gui.modes.page_helpers import throwError
from spm_control.analysis import TTTR_Processor


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

        self.active_folder = None
        self.active_file = None
        self.active_position = None
        self.last_result = None
        self.error = None
        self.status = "idle"
        self.acquisition_ms = 0
        self.start_time = None

        self.mode = None
        self.delay_min_ps = None
        self.bin_width_ps = None
        self.delay_max_ps = None
        self.pulse_delay_min = None
        self.pulse_bin_width = None
        self.pulse_delay_max = None
        self.cygwin_bash = None
        self.photon_gn = None

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def get_active_file(self):
        return self.active_file

    def get_status(self):
        return self.status

    def start(self):
        try:
            if self.is_running():
                raise RuntimeError("A TTTR measurement is already running.")

            tttr_settings = core_config.load_named_settings("tttr", core_config.SCAN_CONFIG)
            scan_settings = core_config.load_named_settings("scan", core_config.SCAN_CONFIG)
            move_settings = core_config.load_named_settings("move", core_config.SCAN_CONFIG)

            self.mode = str(tttr_settings.get("mode", "t2")).lower()

            acquisition_s = float(tttr_settings["acquisition_time"])
            self.acquisition_ms = int(acquisition_s * 1000)

            self.delay_min_ps = int(float(tttr_settings["delay_min"]))
            self.bin_width_ps = int(float(tttr_settings["bin_width"]))
            self.delay_max_ps = int(float(tttr_settings["delay_max"]))

            self.pulse_delay_min = float(tttr_settings.get("pulse_delay_min", -1.5))
            self.pulse_bin_width = float(tttr_settings.get("pulse_bin_width", 0.3))
            self.pulse_delay_max = float(tttr_settings.get("pulse_delay_max", 1.5))

            self.cygwin_bash = Path(tttr_settings.get("cygwin_bash", r"C:\cygwin64\bin\bash.exe"))
            self.photon_gn = str(tttr_settings.get("photon_gn", "/usr/local/bin/photon_gn"))

            if self.mode not in self.MODE_MAP:
                raise ValueError(f"Unsupported TTTR mode: {self.mode}")

            if self.acquisition_ms <= 0:
                raise ValueError("Acquisition time must be greater than zero.")

            if self.delay_min_ps >= self.delay_max_ps:
                raise ValueError("Delay Min must be smaller than Delay Max.")

            if self.bin_width_ps <= 0:
                raise ValueError("Time Bin Width must be greater than zero.")

            if not self.cygwin_bash.is_file():
                raise FileNotFoundError(f"Cygwin Bash was not found: {self.cygwin_bash}")

            x = float(move_settings["x"])
            y = float(move_settings["y"])

            today = datetime.today().strftime("%Y-%m-%d")
            tttr_root = Path(scan_settings["folder_path"]) / today / "tttr"
            tttr_root.mkdir(parents=True, exist_ok=True)

            measurement_number = get_tttr_num(tttr_root)
            acquisition_text = f"{acquisition_s:g}"
            folder_name = f"n{measurement_number}_{self.mode.upper()}_x{x:.3f}_y{y:.3f}_aq{acquisition_text}s"

            self.active_folder = tttr_root / folder_name

            if self.active_folder.exists():
                raise FileExistsError(f"TTTR folder already exists: {self.active_folder}")

            self.active_folder.mkdir()
            self.active_file = self.active_folder / "raw.out"
            self.active_position = {"x": x, "y": y}

            self.stop_event.clear()
            self.last_result = None
            self.error = None
            self.status = "starting"
            self.start_time = None

            if self.time_manager is not None:
                self.time_manager.start(total_units=self.acquisition_ms)

            self.thread = threading.Thread(target=self._run, daemon=True, name="TTTRWorker")
            self.thread.start()
            self.gui_root.after(100, self._update_time)

            return self.active_file

        except Exception as error:
            self.error = error
            self.status = "error"
            print(f"TTTR measurement failed: {error}")
            self.gui_root.after(0, throwError, str(error))

    def _run(self):
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
                    if self.mode == "t2":
                        sync_rate, count_rates = detector.manager.get_rates()

                        print(f"Sync rate: {sync_rate:,} counts/s")

                        for channel, count_rate in enumerate(count_rates):
                            print(f"Channel {channel} rate: {count_rate:,} counts/s")
                        detector.manager.t2_meas(
                            filename=str(self.active_file),
                            tacq=self.acquisition_ms
                        )
                    else:
                        raise NotImplementedError(
                            "T3 acquisition is not implemented yet."
                        )
                finally:
                    self.hardware_manager.set_operation("idle")

            self.start_time = None

            if self.stop_event.is_set():
                self.status = "stopped"
                return

            self.status = "processing"
            print("TTTR acquisition complete. Decoding raw file...")

            decoded_file = self.active_folder / "photons.csv"
            correlation_file = self.active_folder / "g2.csv"

            TTTR_Processor.decode_t2_to_csv(
                input_file=self.active_file,
                output_file=decoded_file,
                resolution_ps=1.0
            )

            print("TTTR decoding complete. Running photon_gn...")

            parser_result = TTTR_Processor.run_t2_correlation(
                input_file=decoded_file,
                output_file=correlation_file,
                delay_min_ps=self.delay_min_ps,
                bin_width_ps=self.bin_width_ps,
                delay_max_ps=self.delay_max_ps,
                cygwin_bash=self.cygwin_bash,
                photon_gn=self.photon_gn
            )

            print("TTTR processing complete.")

            if parser_result.stdout:
                print(parser_result.stdout)

            if parser_result.stderr:
                print(parser_result.stderr)

            self.last_result = {
                "mode": self.mode,
                "raw_file": self.active_file,
                "decoded_file": decoded_file,
                "correlation_file": correlation_file,
                "acquisition_ms": self.acquisition_ms
            }

            self.status = "complete"

        except subprocess.CalledProcessError as error:
            self.error = error
            self.status = "error"

            error_text = error.stderr.strip() if error.stderr else str(error)
            print(f"TTTR processing failed: {error_text}")
            self.gui_root.after(0, throwError, error_text)

        except Exception as error:
            self.error = error
            self.status = "error"
            print(f"TTTR measurement failed: {error}")
            self.gui_root.after(0, throwError, str(error))

        finally:
            self.start_time = None
            self.hardware_manager.set_operation("idle")

            if self.time_manager is not None:
                self.gui_root.after(0, self.time_manager.finish)

            self.thread = None

    def _update_time(self):
        if not self.is_running():
            return

        if self.status == "running" and self.start_time is not None and self.time_manager is not None:
            elapsed_s = time.monotonic() - self.start_time
            remaining_s = max(0, self.acquisition_ms / 1000 - elapsed_s)
            self.time_manager.update_known_duration(remaining_s)

        if self.status in {"starting", "connecting", "running"}:
            self.gui_root.after(100, self._update_time)

    def stop(self):
        if not self.is_running():
            return

        self.stop_event.set()
        self.status = "stopping"