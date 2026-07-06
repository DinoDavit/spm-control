from spm_control.gui.modes.raster_scan import Scan_Page
import customtkinter as ctk
from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Application(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("SPM App")

        self.hardware_in_use = False
    
        # Getting max dimensions of monitor
        max_width = self.winfo_screenwidth()
        max_height = self.winfo_screenheight()

        self.geometry(f"{max_width}x{max_height}")

        self.panels = page_helpers.createPanels(self, MAIN_LAYOUT)
        self.build_mode_toolbar()

    def build_mode_toolbar(self):
        modes_loadout = {
            "scan": self.OpenScanMenu,
            # "filter": self.OpenFilterMenu,
            # "magnification": self.OpenZoomMenu,
            # "calendar": self.OpenCalendarMenu,
        }

        button_size = 0.125

        page_helpers.createToolbar(
            self.panels["modes"],
            modes_loadout,
            button_size,
            horizontal=False,
        )

    def OpenScanMenu(self):
        self.raster_scan_page = Scan_Page(self)

        

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()