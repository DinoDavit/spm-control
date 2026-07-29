from spm_control.gui.modes.scan import Scan_Page
from spm_control.gui.modes.explorer import Explorer_Page
from spm_control.gui.modes.machine_learning import ML_Page
from spm_control.gui.modes.TTTR import TTTR_Page

from spm_control.gui.count_display  import Count_Display
from spm_control.gui.time_display  import Time_Display
from spm_control.gui.file_display import FileDisplay
from spm_control.managers.hardware_manager import HardwareManager
from spm_control.managers.time_manager import TimeManager
from spm_control.gui.main_display import MainDisplay

import customtkinter as ctk

from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_page = None

        self.title("SPM App")

        max_width = self.winfo_screenwidth()
        max_height = self.winfo_screenheight()
        self.geometry(f"{max_width}x{max_height}")

        self.panels = page_helpers.createPanels(self, MAIN_LAYOUT)

        self.hardware_manager = HardwareManager()

        self.main_display = MainDisplay(app=self, parent=self.panels["mode_display"])
        self.build_mode_toolbar()
        self.CreateTimeDisplay()

        self.time_manager = TimeManager(
            gui_root=self,
            update_callback=self.time_display.update_time,
            status_callback=self.time_display.update_status
        )

        self.CreateCountDisplay()
        self.CreateFileDisplay()

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def build_mode_toolbar(self):
        modes_loadout = {
            "scan": self.OpenScanMenu,
            "ML": self.OpenMLMenu,
            "folders": self.OpenExplorerMenu,
            "g2_better": self.OpenTTTRMenu
        }

        page_helpers.createToolbar(
            self.panels["modes"],
            modes_loadout,
            0.125,
            horizontal=False
        )


    def open_page(self, page_class):
        self.cleanup_current_page()
        self.current_page = page_class(self)
        return self.current_page

    def cleanup_current_page(self):
        if self.current_page is not None and hasattr(self.current_page, "cleanup"):
            self.current_page.cleanup()

    def OpenScanMenu(self):
        self.Scan_page = self.open_page(Scan_Page)

    def OpenExplorerMenu(self):
        self.Explorer_page = self.open_page(Explorer_Page)

    def OpenMLMenu(self):
        self.ML_page = self.open_page(ML_Page)

    def OpenTTTRMenu(self):
            self.TTTR_page = self.open_page(TTTR_Page)

    def CreateCountDisplay(self):
        self.count_display = Count_Display(self, parent=self.panels["live_display"])

    def CreateTimeDisplay(self):
        self.time_display = Time_Display(self, parent=self.panels["live_display"])

    def CreateFileDisplay(self):
        self.file_display = FileDisplay(self.panels["file_display"])



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