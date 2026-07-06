import sys
from spm_control.gui.modes import page_helpers
from spm_control.gui.modes import config

class Scan_Page():
    def __init__(self, app):
        required_panels = {
            "mode_options",
            "mode_display",
            "option_parameters",
            "counts",
        }

        self.panels = app.panels

        page_helpers.load_required_panels(self, self.panels, required_panels)

        self.app = app
        self.OpenRunMenu()
        self.build_mode_ops()
    
    def OpenFilterMenu(self):
        p = self.option_parameters # main panel/parent
        p.entries = {}

        Scan_Config = "/Users/davitmoreno/Downloads/Compressed/config_files/scan.yaml"

    def OpenRunMenu(self):
        p = self.option_parameters # main panel/parent
        p.entries = {}
        # Storing them in dictionary to later access them all in yaml file under same name
        Scan_Config = "/Users/davitmoreno/Downloads/Compressed/config_files/scan.yaml"

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate = False
        p.title = page_helpers.createLabel(p.title_frame, "Scan Config", sz=24, side="top", y_space=(4, 4))


        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.6, 0.05])
        p.entries["x_min"], p.entries["x_max"] = page_helpers.createRangeInput(p.first_row, "X:")
        p.second_row = page_helpers.createFrame(p, "second_row", [0.1, 0.19, 0.6, 0.05])
        p.entries["y_min"], p.entries["y_max"] = page_helpers.createRangeInput(p.second_row, "Y:")
    
        p.third_row = page_helpers.createFrame(p, "third_row", [0.13, 0.27, 0.4, 0.05])
        p.entries["z_focus"] = page_helpers.createSingleEntry(p.third_row, "Z-focus")

        p.fourth_row = page_helpers.createFrame(p, "third_row", [0.13, 0.34, 0.47, 0.05])
        p.entries["resolution"] = page_helpers.createSingleEntry(p.fourth_row, "Resolution")

        page_helpers.bind_entry(p.entries["x_min"], nextE=p.entries["x_max"], min_val=0, max_val=100, multi=0.2, ranged=True)
        page_helpers.bind_entry(p.entries["x_max"], nextE=p.entries["y_min"], min_val=0, max_val=100, multi=0.2)
        page_helpers.bind_entry(p.entries["y_min"], nextE=p.entries["y_max"], min_val=0, max_val=100, multi=0.2, ranged=True)
        page_helpers.bind_entry(p.entries["y_max"], nextE=p.entries["z_focus"], min_val=0, max_val=100, multi=0.2)
        page_helpers.bind_entry(p.entries["z_focus"], nextE=p.entries["resolution"], min_val=0, max_val=20)
        page_helpers.bind_entry(p.entries["resolution"], min_val=0.2, max_val=25, multi=0.2)

        p.last_row = page_helpers.createFrame(p, "third_row", [0.35, 0.9, 0.3, 0.05])
        p.Run = page_helpers.createButton(p.last_row, "Run", 5, lambda: config.update(p.entries, "scan", Scan_Config))
        
    
    def build_mode_ops(self):
        p = self.mode_options
        options_loadout = {
            "run": self.OpenRunMenu,
            # "filter": self.OpenFilterMenu,
            # "magnification": self.OpenZoomMenu,
            # "calendar": self.OpenCalendarMenu,
        }
        button_size = 0.08

        page_helpers.createToolbar(p, options_loadout, button_size)