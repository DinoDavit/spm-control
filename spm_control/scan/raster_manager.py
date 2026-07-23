import threading

from spm_control.scan.raster import run_raster_scan


class RasterManager:
    def __init__(self):
        self.thread = None
        self.stop_event = threading.Event()

    def start(self):
        if self.is_running():
            raise RuntimeError("A raster scan is already running.")

        self.stop_event.clear()

        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
            name="RasterScanWorker"
        )

        self.thread.start()

    def stop(self):
        self.stop_event.set()

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def _run(self):
        print("Raster scan started.")

        try:
            result = run_raster_scan(
                stop_event=self.stop_event
            )

            if result["stopped"]:
                print("Raster scan stopped safely.")
            else:
                print("Raster scan completed.")

        except Exception as error:
            print(f"Raster scan failed: {error}")

        finally:
            print("Raster scan worker finished.")