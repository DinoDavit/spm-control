from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT
from spm_control.managers.TTTR_manager import TTTRManager
from spm_control.gui.modes.point_selector import PointSelector


from tkinter import messagebox

from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT
from spm_control.managers.TTTR_manager import TTTRManager
from spm_control.gui.modes.point_selector import PointSelector


class TTTR_Page:
    def __init__(self, app):
        required_panels = {"mode_options", "option_parameters"}

        self.app = app
        self.panels = app.panels
        self.selected_xy = None

        # Detect an existing displayed plot without reloading mode_display.
        try:
            display = self.panels["mode_display"]
            canvas = display.canvas
            axes = display.axes
        except (KeyError, AttributeError):
            messagebox.showerror(
                "No Plot Displayed",
                "Please display a scan before opening the TTTR point-selection menu."
            )
            raise RuntimeError("TTTR requires an active scan plot")

        if canvas is None or axes is None:
            messagebox.showerror(
                "No Plot Displayed",
                "Please display a scan before opening the TTTR point-selection menu."
            )
            raise RuntimeError("TTTR requires an active scan plot")

        self.tttr_manager = TTTRManager(
            gui_root=app,
            hardware_manager=app.hardware_manager,
            time_manager=app.time_manager
        )

        page_helpers.reload_panels(
            self.panels,
            MAIN_LAYOUT,
            required_panels,
            notMain=True
        )
        page_helpers.load_required_panels(
            self,
            self.panels,
            required_panels
        )

        self.point_selector = PointSelector(
            canvas=canvas,
            axes=axes,
            callback=self.point_selected
        )

        self.OpenTTTRMenu()
        self.build_mode_ops()

    def begin_point_selection(self):
        self.point_selector.enable()

    def point_selected(self, point):
        self.selected_xy = point
        print("Selected TTTR point:", point)

    def OpenTTTRMenu(self):
        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate(False)
        p.title = page_helpers.createLabel(p.title_frame, "TTTR Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.7, 0.05])
        p.entries["Acquisition Time"] = page_helpers.createSingleEntry(
            p.first_row, "Acquisition Time (s)", numbered_entry=True, placeholder="e.g. 1200"
        )

        p.second_row = page_helpers.createFrame(p, "second_row", [0.1, 0.2, 0.5, 0.08])
        p.mode = page_helpers.createSelection(p.second_row, ["T2", "T3"], spacing=6)

        p.third_row = page_helpers.createFrame(p, "third_row", [0.1, 0.3, 0.5, 0.08])
        p.select_point = page_helpers.createButton(
            p.third_row,
            "Select Point",
            5,
            self.begin_point_selection
        )

        self.parameter_panel = p

    def OpenPlotterMenu(self):
        print("HELLO WORLD")

    def build_mode_ops(self):
        options_loadout = {
            "select_point": self.OpenTTTRMenu,
            "g2_plot": self.OpenPlotterMenu,
        }

        page_helpers.createToolbar(self.mode_options, options_loadout, 0.08)