import threading


class CountManager:
    def __init__(self, gui_root, hardware_manager, update_callback=None, status_callback=None, interval=0.5):
        self.gui_root = gui_root
        self.hardware_manager = hardware_manager
        self.update_callback = update_callback
        self.status_callback = status_callback
        self.interval = interval

        self.thread = None
        self.stop_event = threading.Event()

        self.last_counts = (0, 0)
        self.error = None

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

    def get_last_counts(self):
        return self.last_counts

    def start(self):
        if self.is_running():
            return

        self.stop_event.clear()
        self.error = None

        self.thread = threading.Thread(target=self._run, daemon=True, name="IdleCountWorker")
        self.thread.start()

    def stop(self):
        self.stop_event.set()

    def _publish_counts(self, ch1, ch2):
        self.last_counts = (ch1, ch2)

        if self.update_callback is not None:
            self.gui_root.after(0, self.update_callback, ch1, ch2)

    def _publish_status(self, status):
        if self.status_callback is not None:
            self.gui_root.after(0, self.status_callback, status)
            # Callback function as soon as it it basically can and publishes status
            # 

    def _run(self):
        try:
            self.hardware_manager.connect_detector()

            while not self.stop_event.is_set():
                operation = self.hardware_manager.get_operation()

                if operation != "idle":
                    self._publish_status(operation)
                    self.stop_event.wait(self.interval)
                    continue

                acquired = self.hardware_manager.detector_lock.acquire(
                    blocking=False
                )

                if acquired:
                    try:
                        # Always fetch the current detector.
                        detector = self.hardware_manager.detector

                        if detector is None:
                            self._publish_status("disconnected")
                            continue

                        counts = detector.poll_counts()

                        if len(counts) < 2:
                            raise RuntimeError(
                                "Expected two detector channels, "
                                f"received: {counts}"
                            )

                        ch1 = int(counts[0])
                        ch2 = int(counts[1])

                    finally:
                        self.hardware_manager.detector_lock.release()

                    self._publish_counts(ch1, ch2)

                else:
                    self._publish_status(
                        self.hardware_manager.get_operation()
                    )

                self.stop_event.wait(self.interval)

        except Exception as error:
            self.error = error
            self._publish_status("error")
            print(f"Idle count monitoring failed: {error}")