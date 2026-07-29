from spm_control.gui.modes import page_helpers
from spm_control.gui.modes import config
from spm_control.gui.layout import MAIN_LAYOUT
from spm_control.work_in_progress_legacy_scripts import filter_scan
from spm_control.managers.raster_manager import RasterManager

from pathlib import Path

import time


class Scan_Page():
    def __init__(self, app):
        required_panels = {
            "mode_display",
            "mode_options",
            "option_parameters",
        }

        self.panels = app.panels

        page_helpers.reload_panels(self.panels, MAIN_LAYOUT, required_panels, notMain=True)
        time.sleep(0.05)  # Wait for the panels to be reloaded before loading required panels
        page_helpers.load_required_panels(self, self.panels, required_panels)

        self.app = app
        self.OpenRunMenu()
        self.build_mode_ops()

    def OpenRunMenu(self):
        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}
        # Storing them in dictionary to later access them all in yaml file under same name
        Scan_Config = Path(__file__).resolve().parents[3] / "config_files" / "scan.yaml"

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate = False
        p.title = page_helpers.createLabel(p.title_frame, "Scan Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.6, 0.05])
        p.entries["x_min"], p.entries["x_max"] = page_helpers.createRangeInput(p.first_row, "X:")
        p.second_row = page_helpers.createFrame(p, "second_row", [0.1, 0.19, 0.6, 0.05])
        p.entries["y_min"], p.entries["y_max"] = page_helpers.createRangeInput(p.second_row, "Y:")
        p.third_row = page_helpers.createFrame(p, "third_row", [0.13, 0.27, 0.4, 0.05])
        p.entries["z_focus"] = page_helpers.createSingleEntry(p.third_row, "Z-focus")
        p.fourth_row = page_helpers.createFrame(p, "third_row", [0.13, 0.34, 0.47, 0.05])
        p.entries["resolution"] = page_helpers.createSingleEntry(p.fourth_row, "Resolution")

        page_helpers.bind_entry(p.entries["x_min"], nextE=p.entries["x_max"], min_val=0, max_val=100, ranged=True)
        page_helpers.bind_entry(p.entries["x_max"], nextE=p.entries["y_min"], min_val=0, max_val=100)
        page_helpers.bind_entry(p.entries["y_min"], nextE=p.entries["y_max"], min_val=0, max_val=100, ranged=True)
        page_helpers.bind_entry(p.entries["y_max"], nextE=p.entries["z_focus"], min_val=0, max_val=100)
        page_helpers.bind_entry(p.entries["z_focus"], nextE=p.entries["resolution"], min_val=0, max_val=20)
        page_helpers.bind_entry(p.entries["resolution"], min_val=0.2, max_val=25)


        self.raster_manager = RasterManager(self.app, self.app.hardware_manager, time_manager=self.app.time_manager)
        p.RunFrame = page_helpers.createFrame(p, "third_row", [0.2, 0.9, 0.25, 0.05])
        p.Run = page_helpers.createButton(p.RunFrame, "Run", 5, lambda: config.update(p.entries, "scan", Scan_Config, nextCall=self.start_scan))

        p.StopFrame = page_helpers.createFrame(p, "third_row", [0.5, 0.9, 0.25, 0.05])
        confirm_msg = "Please confirm you want to stop the scan, data will not be saved!"
        def stop_scan():
            self.raster_manager.stop()
        p.Stop = page_helpers.createButton(p.StopFrame, "Stop", 5, lambda: page_helpers.confirmation(confirm_msg, nextCall=stop_scan), color="#c62828", hcolor="#8B0000")

    def start_scan(self):
        try:
            self.raster_manager.start()
        except Exception as error:
            page_helpers.throwError(str(error))

    def OpenFilterMenu(self):
        ch = 0
        file_path = page_helpers.get_file(self.app.file_display)

        path = Path(file_path)
        stem = path.stem

        if stem.endswith("_scan_data"):
            base = stem.removesuffix("_scan_data")
        elif stem.endswith("_ch1"):
            base = stem.removesuffix("_ch1")
            ch = 1
        elif stem.endswith("_ch2"):
            base = stem.removesuffix("_ch2")
            ch = 2
        else:
            if ("pq" not in stem):
                page_helpers.throwError("Please select a valid raster scan file.")
            base = stem

        data_path = path.parent / f"{base}_scan_data.txt"

        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}

        Scan_Data = page_helpers.get_file(self.app.file_display)
        Scan_Config = Path(__file__).resolve().parents[3] / "config_files" / "scan.yaml"

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate = False
        p.title = page_helpers.createLabel(p.title_frame, "Filter Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.7, 0.05])
        p.entries["intensity_min"], p.entries["intensity_max"] = page_helpers.createRangeInput(p.first_row, "Intensity:")

        page_helpers.bind_entry(p.entries["intensity_min"], nextE=p.entries["intensity_max"], min_val=0, max_val=1e10, multi=1, ranged=True, emptyOk=True)
        page_helpers.bind_entry(p.entries["intensity_max"], min_val=0.1, max_val=1e10, multi=1, emptyOk=True)

        

        def display_filtered_scan(file_path, channel):
            fig = filter_scan.create_filtered_scan_plot(file_path, int(channel))
            self.app.main_display.display_plot(fig, source="filtered_raster")
            
        p.last_row = page_helpers.createFrame(p, "third_row", [0.35, 0.9, 0.3, 0.05])
        p.Filter = page_helpers.createButton(p.last_row, "Filter", 5, 
                                                lambda: config.update(p.entries, "scan", Scan_Config, nextCall = 
                                                                    lambda: display_filtered_scan(data_path, ch)))

    def OpenZoomMenu(self):
        Scan_Config = Path(__file__).resolve().parents[3] / "config_files" / "scan.yaml"

        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}
        
        Scan_Data = "/Users/davitmoreno/Downloads/Compressed/config_files/scan.yaml"
        #print("Will add zoom input stuff that will fetch the metadata of file or something...")

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate = False
        p.title = page_helpers.createLabel(p.title_frame, "Zoom Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.6, 0.05])
        p.entries["x"]= page_helpers.createSingleEntry(p.first_row, "x (µm)", "ex 30.2", numbered_entry=True, min_val=0, max_val=100)
        p.second_row = page_helpers.createFrame(p, "second_row", [0.1, 0.19, 0.6, 0.05])
        p.entries["y"] = page_helpers.createSingleEntry(p.second_row, "y (µm)", "ex 80.5", numbered_entry=True, min_val=0, max_val=100)
        p.third_row = page_helpers.createFrame(p, "third_row", [0.1, 0.26, 0.6, 0.05])
        p.entries["z"] = page_helpers.createSingleEntry(p.third_row, "z-focus (µm)", "ex 10.2", numbered_entry=True)
        p.fourth_row = page_helpers.createFrame(p, "fourth_row", [0.1, 0.5, 0.6, 0.05])
        p.move = page_helpers.createButton(p.fourth_row, "Move Piezo-Stage", 5, lambda: config.update(p.entries, "move", Scan_Config, 
                                                                                         nextCall=self.raster_manager.move_piezo))



        page_helpers.bind_entry(p.entries["x"], nextE=p.entries["y"], min_val=0, max_val=100, ranged=True)
        page_helpers.bind_entry(p.entries["y"], nextE=p.entries["z"], min_val=0, max_val=100, ranged=True)
        page_helpers.bind_entry(p.entries["z"], min_val=0, max_val=20)
    def build_mode_ops(self):
        p = self.mode_options
        options_loadout = {
            "run": self.OpenRunMenu,
            "filter": self.OpenFilterMenu,
            "magnification": self.OpenZoomMenu,
        }
        button_size = 0.08

        page_helpers.createToolbar(p, options_loadout, button_size)