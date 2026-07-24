import os
import threading
from datetime import datetime
from pathlib import Path

import numpy as np

import spm_control.config as config
from spm_control.scan import scan_plot_and_analysis as spa
from spm_control.hardware.piezo_stage import PIStage
from spm_control.hardware.hydraharp import HydraHarpDetector
from spm_control.scan.raster import run_raster_scan


def get_exp_num(folder_path, suffix="_pq"):
    today = datetime.today().strftime("%Y-%m-%d")
    most_recent = 0

    for file_name in os.listdir(folder_path):
        if file_name.endswith("_scan_data.txt") and file_name.startswith(today + suffix):
            number = file_name.removeprefix(today + suffix).split("_")[0]

            if number.isdigit():
                most_recent = max(most_recent, int(number))

    return most_recent + 1


class RasterManager:
    def __init__(self, gui_root):
        self.gui_root = gui_root
        self.thread = None
        self.stop_event = threading.Event()

        self.active_file = None
        self.active_data = None
        self.last_result = None
        self.error = None

        self.raster_figure = None
        self.raster_image = None
        self.raster_colorbar = None

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def get_active_data(self):
        return self.active_data

    def clear_live_plot(self):
        self.raster_figure = None
        self.raster_image = None
        self.raster_colorbar = None

    def publish_raster_update(self, intensities):
        if (
            self.raster_figure is None
            or self.raster_image is None
            or self.raster_colorbar is None
        ):
            return

        self.gui_root.after(
            0,
            spa.update_live_raster_plot,
            self.raster_figure,
            self.raster_image,
            self.raster_colorbar,
            intensities.copy()
        )

    def start(self):
        if self.is_running():
            raise RuntimeError("A raster scan is already running.")

        scan_settings = config.load_named_settings("scan", config.SCAN_CONFIG)

        x_min = scan_settings["x_min"]
        x_max = scan_settings["x_max"]
        y_min = scan_settings["y_min"]
        y_max = scan_settings["y_max"]
        resolution = scan_settings["resolution"]

        if resolution <= 0:
            raise ValueError("Raster resolution must be greater than zero.")

        x_nodes = np.linspace(x_min, x_max, int((x_max - x_min) / resolution) + 1).round(3)
        y_nodes = np.linspace(y_min, y_max, int((y_max - y_min) / resolution) + 1).round(3)

        today = datetime.today().strftime("%Y-%m-%d")
        scan_folder = Path(scan_settings["folder_path"]) / today
        scan_folder.mkdir(parents=True, exist_ok=True)

        experiment_number = get_exp_num(scan_folder)
        scan_name = f"{today}_pq{experiment_number}"

        self.active_file = scan_folder / f"{scan_name}_scan_data.txt"

        combined_png = scan_folder / f"{scan_name}.png"
        ch1_png = scan_folder / f"{scan_name}_ch1.png"
        ch2_png = scan_folder / f"{scan_name}_ch2.png"

        if self.active_file.exists():
            raise FileExistsError(f"Scan file already exists: {self.active_file}")

        self.raster_figure, self.raster_image, self.raster_colorbar = (
            spa.create_live_raster_plot(
                xlim=(x_nodes[0], x_nodes[-1]),
                ylim=(y_nodes[0], y_nodes[-1]),
                shape=(len(x_nodes), len(y_nodes))
            )
        )

        self.active_data = {
            "type": "raster",
            "experiment_number": experiment_number,
            "scan_name": scan_name,
            "folder": scan_folder,
            "data_file": self.active_file,
            "combined_png": combined_png,
            "ch1_png": ch1_png,
            "ch2_png": ch2_png,
            "x_nodes": x_nodes,
            "y_nodes": y_nodes,
            "figure": self.raster_figure,
            "status": "starting"
        }

        self.stop_event.clear()
        self.last_result = None
        self.error = None

        self.thread = threading.Thread(target=self._run, daemon=True, name="RasterScanWorker")
        self.thread.start()

        return self.active_data

    def stop(self):
        self.stop_event.set()

    def _save_scan_plots(self):
        intensities = self.last_result["intensities"]
        split_intensities = self.last_result["split_intensities"]
        x_nodes = self.last_result["x_nodes"]
        y_nodes = self.last_result["y_nodes"]

        spa.save_raster_plot(
            intensities,
            x_nodes,
            y_nodes,
            self.active_data["combined_png"],
            "Combined Channels"
        )

        spa.save_raster_plot(
            split_intensities[0],
            x_nodes,
            y_nodes,
            self.active_data["ch1_png"],
            "Channel 1"
        )

        spa.save_raster_plot(
            split_intensities[1],
            x_nodes,
            y_nodes,
            self.active_data["ch2_png"],
            "Channel 2"
        )

    def _run(self):
        stage = None
        detector = None

        try:
            self.active_data["status"] = "connecting"

            stage_settings = config.load_named_settings("stage", config.HARDWARE_CONFIG)
            hydraharp_settings = config.load_named_settings("hydraharp", config.HARDWARE_CONFIG)
            sync_settings = config.load_named_settings("sync", config.HARDWARE_CONFIG)

            stage = PIStage(
                stage_settings["CONTROLLER_NAME"],
                str(stage_settings["SERIAL_NUM"]),
                [stage_settings["STAGE_MODEL"]] * stage_settings["NUM_AXES"]
            )

            detector = HydraHarpDetector(hydraharp_settings, sync_settings)

            stage.connect()
            detector.connect()

            self.active_data["status"] = "running"

            self.last_result = run_raster_scan(
                stage,
                detector,
                self.stop_event,
                self.active_file,
                progress_callback=self.publish_raster_update
            )

            self.publish_raster_update(self.last_result["intensities"])

            self.active_data["status"] = "saving"
            self._save_scan_plots()

            if self.last_result.get("stopped", False):
                self.active_data["status"] = "stopped"
            else:
                self.active_data["status"] = "complete"

        except Exception as error:
            self.error = error

            if self.active_data is not None:
                self.active_data["status"] = "error"

            print(f"Raster scan failed: {error}")

        finally:
            if detector is not None:
                try:
                    detector.close()
                except Exception as error:
                    print(f"HydraHarp close failed: {error}")

            if stage is not None:
                try:
                    stage.close()
                except Exception as error:
                    print(f"Stage close failed: {error}")