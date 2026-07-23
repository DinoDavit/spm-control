import threading

from spm_control.gui.modes import config
from spm_control.hardware.piezo_stage import PiezoStage
from spm_control.hardware.hydraharp import HydraHarpDetector
from spm_control.scan.raster import run_raster_scan


class RasterManager:
    def __init__(self):
        self.thread = None
        self.stop_event = threading.Event()

    def start(self):
        if self.is_running():
            raise RuntimeError("A raster scan is already running.")

        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run, daemon=True, name="RasterScanWorker")
        self.thread.start()

    def stop(self):
        self.stop_event.set()

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def _run(self):
        stage = None
        detector = None

        try:
            stage_settings = config.load_named_settings("stage", config.HARDWARE_CONFIG)
            hydraharp_settings = config.load_named_settings("hydraharp", config.HARDWARE_CONFIG)
            sync_settings = config.load_named_settings("sync", config.HARDWARE_CONFIG)

            stage = PiezoStage(stage_settings)
            detector = HydraHarpDetector(hydraharp_settings, sync_settings)

            print("Connecting piezo stage...")
            stage.connect()

            print("Connecting HydraHarp...")
            detector.connect()

            result = run_raster_scan(stage, detector, self.stop_event)

            if result["stopped"]:
                print("Raster scan stopped safely.")
            else:
                print("Raster scan completed.")

        except Exception as error:
            print(f"Raster scan failed: {error}")

        finally:
            if detector is not None:
                try:
                    detector.close()
                    print("HydraHarp closed.")
                except Exception as error:
                    print(f"HydraHarp cleanup failed: {error}")

            if stage is not None:
                try:
                    stage.close()
                    print("Piezo stage closed.")
                except Exception as error:
                    print(f"Piezo cleanup failed: {error}")

            print("Raster scan worker finished.")