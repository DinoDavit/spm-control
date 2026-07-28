from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT
import time


class TTTR_Page:
    def __init__(self, app):
        required_panels = {
            "mode_options",
            "mode_display",
            "option_parameters",
        }

        self.panels = app.panels
        page_helpers.reload_panels(self.panels, MAIN_LAYOUT, required_panels, notMain=True)
        time.sleep(0.05)
        page_helpers.load_required_panels(self, self.panels, required_panels)

        self.app = app
        self.OpenTTTRMenu()

    def OpenTTTRMenu(self):
        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate(False)
        p.title = page_helpers.createLabel(p.title_frame, "TTTR Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.7, 0.05])
        p.entries["Aquisition Time"] = page_helpers.createSingleEntry(
            p.first_row, "Aquisition Time (s)", numbered_entry=True, placeholder="e.g. 1200"
        )

        p.second_row = page_helpers.createFrame(p, "first_row", [0.1, 0.2, 0.5, 0.08])
        p.mode = page_helpers.createSelection(p.second_row, ["T2", "T3"])
