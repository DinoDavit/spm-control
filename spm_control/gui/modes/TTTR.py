from tkinter import messagebox

from spm_control.gui.modes import config, page_helpers
from spm_control.gui.layout import MAIN_LAYOUT
from spm_control.gui.modes.point_selector import PointSelector
from spm_control.managers.TTTR_manager import TTTRManager
from spm_control.managers.raster_manager import RasterManager

import spm_control.core_config as core_config


class TTTR_Page:
    def __init__(self, app):
        required_panels = {"mode_options", "option_parameters", "mode_display"}

        self.app = app
        self.panels = app.panels
        self.selected_xy = None
        self.Scan_Config = core_config.SCAN_CONFIG
        self.Hardware_Config = core_config.HARDWARE_CONFIG

        try:
            canvas, axes = app.main_display.get_active_plot()
        except RuntimeError as error:
            messagebox.showerror("No Active Plot", str(error), parent=app)
            raise

        self.tttr_manager = TTTRManager(gui_root=app, hardware_manager=app.hardware_manager, time_manager=app.time_manager)
        self.raster_manager = RasterManager(app, app.hardware_manager, time_manager=app.time_manager)

        page_helpers.reload_panels(self.panels, MAIN_LAYOUT, required_panels, notMain=True)
        page_helpers.load_required_panels(self, self.panels, required_panels)

        self.point_selector = PointSelector(canvas=canvas, axes=axes, callback=self.point_selected)

        self.OpenTTTRMenu()
        self.build_mode_ops()

    def begin_point_selection(self):
        self.point_selector.enable()

    def point_selected(self, point):
        try:
            x, y = map(float, point)
            self.selected_xy = (x, y)

            scan_settings = core_config.load_named_settings("scan", self.Scan_Config)
            position = {"x": x, "y": y, "z": float(scan_settings["z_focus"])}

            config.update_selection(position, "move", self.Scan_Config, nextCall=self.raster_manager.move_piezo)
            print(f"Selected TTTR point: ({x:.3f}, {y:.3f})")

        except Exception as error:
            page_helpers.throwError(str(error))

    def begin_measurement(self):
        if self.selected_xy is None:
            page_helpers.throwError("Please select a point before beginning the measurement.")
            return

        try:
            acquisition_entry = self.parameter_panel.entries["acquisition_time"].get()

            if not acquisition_entry:
                raise ValueError("Please enter an acquisition time.")

            acquisition_s = float(acquisition_entry)

            if acquisition_s <= 0:
                raise ValueError("Acquisition time must be greater than zero.")

            self.tttr_manager.start(acquisition_ms=int(acquisition_s * 1000))

        except Exception as error:
            page_helpers.throwError(str(error))

    def stop_measurement(self):
        try:
            self.tttr_manager.stop()
        except Exception as error:
            page_helpers.throwError(str(error))

    def mode_changed(self, mode):
        if mode == "T3":
            self.parameter_panel.t3_options.place(relx=0.1, rely=0.28, relwidth=0.6, relheight=0.08)
            selected_mode = "t3"
        else:
            self.parameter_panel.t3_options.place_forget()
            selected_mode = "t2"

        config.update_selection({"default_mode": selected_mode}, "hydraharp", self.Hardware_Config)

    def OpenTTTRMenu(self):
        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate(False)
        p.title = page_helpers.createLabel(p.title_frame, "TTTR Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.7, 0.05])
        p.entries["acquisition_time"] = page_helpers.createSingleEntry(p.first_row, "Acquisition Time (s)", numbered_entry=True, placeholder="e.g. 1200")
        page_helpers.bind_entry(p.entries["acquisition_time"], min_val=0.001, max_val=36000)

        p.second_row = page_helpers.createFrame(p, "second_row", [0.1, 0.2, 0.5, 0.08])
        p.mode = page_helpers.createSelection(p.second_row, ["T2", "T3"], default="T2", command=self.mode_changed, spacing=6)

        p.t3_options = page_helpers.createFrame(p, "t3_options", [0.1, 0.32, 0.6, 0.08])
        p.entries["binning"] = page_helpers.createSingleEntry(p.t3_options, "Binning", numbered_entry=True, placeholder="e.g. 4")
        page_helpers.bind_entry(p.entries["binning"], min_val=0, max_val=16)
        p.t3_options.place_forget()

        p.third_row = page_helpers.createFrame(p, "third_row", [0.0625, 0.9, 0.25, 0.05])
        p.select_point = page_helpers.createButton(p.third_row, "Select Point", 5, self.begin_point_selection)

        p.fourth_row = page_helpers.createFrame(p, "fourth_row", [0.375, 0.9, 0.25, 0.05])
        p.take_measurement = page_helpers.createButton(p.fourth_row, "Measure", 5, self.begin_measurement, color="green", hcolor="#14532D")

        p.fifth_row = page_helpers.createFrame(p, "fifth_row", [0.6875, 0.9, 0.25, 0.05])
        p.stop_measurement = page_helpers.createButton(p.fifth_row, "Stop", 5, self.stop_measurement, color="red", hcolor="#7F1D1D")

        self.parameter_panel = p
        self.mode_changed("T2")

    def OpenPlotterMenu(self):
        print("TTTR plotter menu not implemented yet.")

    def build_mode_ops(self):
        options_loadout = {"select_point": self.OpenTTTRMenu, "g2_plot": self.OpenPlotterMenu}
        page_helpers.createToolbar(self.mode_options, options_loadout, 0.08)

    def cleanup(self):
        if hasattr(self, "point_selector"):
            self.point_selector.cleanup()