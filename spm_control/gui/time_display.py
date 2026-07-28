from spm_control.gui.modes import page_helpers


class Time_Display:
    def __init__(self, app, parent):
        self.app = app
        self.parent = parent

        self.est_frame = page_helpers.createFrame(
            parent, "est_time", [0.05, 0.65, 0.9, 0.32],
            outline=True
        )

        self.est_entry, self.est_value = page_helpers.createDisplayEntry(
            self.est_frame,
            "Estimated Time",
            value="--:--",
            color="red"
        )

    def update_time(self, seconds):
        formatted = self.format_time(seconds)
        print("Updating visible time to:", formatted)
        self.est_value.set(formatted)

    def update_status(self, status):
        status_messages = {
            "calculating": "CALCULATING",
            "saving": "SAVING",
            "finished": "00:00",
            "idle": "--:--",
            "error": "ERROR"
        }

        message = status_messages.get(status)
        if message is not None:
            self.est_value.set(message)

    @staticmethod
    def format_time(seconds):
        if seconds is None:
            return "--:--"

        seconds = max(0, int(seconds))
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"

        return f"{minutes:02d}:{seconds:02d}"