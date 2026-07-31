import time


class TimeManager:
    def __init__(self, gui_root, update_callback=None, status_callback=None):
        self.gui_root = gui_root
        self.update_callback = update_callback
        self.status_callback = status_callback

        self.start_time = None
        self.total_units = None
        self.completed_units = 0

    def start(self, total_units=None):
        self.start_time = time.monotonic()
        self.total_units = total_units
        self.completed_units = 0

        self.publish_time(None)
        self.publish_status("calculating")

    def update(self, completed_units):
        if self.start_time is None:
            return

        self.completed_units = completed_units

        if completed_units < 10:
            self.publish_status("calculating")
            return

        elapsed = time.monotonic() - self.start_time
        average_time = elapsed / completed_units
        remaining = average_time * (self.total_units - completed_units)

        self.publish_time(remaining)

    def update_known_duration(self, remaining_seconds):
        if self.start_time is None:
            return

        self.publish_time(remaining_seconds)

    def finish(self):
        self.publish_time(0)
        self.publish_status("finished")
        self.reset_state()

    def clear(self):
        self.publish_time(None)
        self.publish_status("idle")
        self.reset_state()

    def error(self):
        self.publish_time(None)
        self.publish_status("error")
        self.reset_state()

    def reset_state(self):
        self.start_time = None
        self.total_units = None
        self.completed_units = 0

    def publish_time(self, seconds):
        if self.update_callback is not None:
            self.gui_root.after(0, self.update_callback, seconds)

    def publish_status(self, status):
        if self.status_callback is not None:
            self.gui_root.after(0, self.status_callback, status)