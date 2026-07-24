from spm_control.gui.modes import page_helpers
from spm_control.managers.count_manager import CountManager


class Live_Display:
    def __init__(self, app, parent):
        self.app = app
        self.parent = parent

        self.ch1_frame = page_helpers.createFrame(
            parent,
            "channel_1",
            [0.05, 0.08, 0.9, 0.4],
            outline=True
        )

        self.ch2_frame = page_helpers.createFrame(
            parent,
            "channel_2",
            [0.05, 0.52, 0.9, 0.4],
            outline=True
        )

        self.ch1_entry, self.ch1_value = page_helpers.createDisplayEntry(
            self.ch1_frame,
            "Channel 1"
        )

        self.ch2_entry, self.ch2_value = page_helpers.createDisplayEntry(
            self.ch2_frame,
            "Channel 2"
        )

        self.count_manager = CountManager(
            app,
            app.hardware_manager,
            self.update_counts,
            interval=0.5
        )

        self.count_manager.start()

    def update_counts(self, ch1, ch2):
        self.ch1_value.set(self.format_count(ch1))
        self.ch2_value.set(self.format_count(ch2))

    @staticmethod
    def format_count(count):
        if abs(count) < 10000:
            return str(count)

        coefficient, exponent = f"{count:.2e}".split("e")
        coefficient = coefficient.rstrip("0").rstrip(".")
        return f"{coefficient}e{int(exponent)}"