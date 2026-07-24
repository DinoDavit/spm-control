from spm_control.gui.modes.scan import Scan_Page
from spm_control.gui.modes.explorer import Explorer_Page
from spm_control.gui.modes.machine_learning import ML_Page
from spm_control.gui.live_display import Live_Display
from spm_control.managers.hardware_manager import HardwareManager

import customtkinter as ctk

from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SPM App")

        max_width = self.winfo_screenwidth()
        max_height = self.winfo_screenheight()
        self.geometry(f"{max_width}x{max_height}")

        self.hardware_manager = HardwareManager()

        self.panels = page_helpers.createPanels(self, MAIN_LAYOUT)
        self.build_mode_toolbar()
        self.CreateLiveDisplay()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def build_mode_toolbar(self):
        modes_loadout = {
            "scan": self.OpenScanMenu,
            "ML": self.OpenMLMenu,
            "folders": self.OpenExplorerMenu,
        }

        page_helpers.createToolbar(
            self.panels["modes"],
            modes_loadout,
            0.125,
            horizontal=False
        )

    def OpenScanMenu(self):
        self.Scan_page = Scan_Page(self)

    def OpenExplorerMenu(self):
        self.Explorer_page = Explorer_Page(self)

    def OpenMLMenu(self):
        self.ML_page = ML_Page(self)

    def CreateLiveDisplay(self):
        self.live_display = Live_Display(self)

    def close_app(self):
        if hasattr(self, "live_display"):
            self.live_display.count_manager.stop()

            thread = self.live_display.count_manager.thread
            if thread is not None and thread.is_alive():
                thread.join(timeout=2)

        if hasattr(self, "hardware_manager"):
            self.hardware_manager.close_detector()

        self.destroy()


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()