import sys
from spm_control.gui.modes import page_helpers
from spm_control.gui.modes import config
from spm_control.gui.layout import MAIN_LAYOUT
import time
from spm_control.work_in_progress_legacy_scripts import filter_scan
from pathlib import Path
import sys
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Scan_Page():
    def __init__(self, app):
        required_panels = {
            "mode_options",
            "mode_display",
            "option_parameters",
            "counts",
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

        page_helpers.bind_entry(p.entries["x_min"], nextE=p.entries["x_max"], min_val=0, max_val=100, multi=0.2, ranged=True)
        page_helpers.bind_entry(p.entries["x_max"], nextE=p.entries["y_min"], min_val=0, max_val=100, multi=0.2)
        page_helpers.bind_entry(p.entries["y_min"], nextE=p.entries["y_max"], min_val=0, max_val=100, multi=0.2, ranged=True)
        page_helpers.bind_entry(p.entries["y_max"], nextE=p.entries["z_focus"], min_val=0, max_val=100, multi=0.2)
        page_helpers.bind_entry(p.entries["z_focus"], nextE=p.entries["resolution"], min_val=0, max_val=20)
        page_helpers.bind_entry(p.entries["resolution"], min_val=0.2, max_val=25, multi=0.2)

        p.last_row = page_helpers.createFrame(p, "third_row", [0.35, 0.9, 0.3, 0.05])
        def demo():
            
            run_scan_file = Path(__file__).resolve().parents[2] / "work_in_progress_legacy_scripts" / "run_scan_5.py"

            subprocess.Popen(
            [sys.executable, str(run_scan_file)],
            cwd=str(run_scan_file.parent),)

        p.Run = page_helpers.createButton(p.last_row, "Run", 5, lambda: config.update(p.entries, "scan", Scan_Config, nextCall=lambda: (demo())))

    def OpenFilterMenu(self):
        ch = 0
        file_path = page_helpers.get_file(self.panels)

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
            if ("run" not in stem):
                page_helpers.throwError("Please select a valid raster scan file.")
            base = stem

        data_path = path.parent / f"{base}_scan_data.txt"

        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}

        Scan_Data = page_helpers.get_file(self.panels)
        Scan_Config = Path(__file__).resolve().parents[3] / "config_files" / "scan.yaml"

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate = False
        p.title = page_helpers.createLabel(p.title_frame, "Filter Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.7, 0.05])
        p.entries["intensity_min"], p.entries["intensity_max"] = page_helpers.createRangeInput(p.first_row, "Intensity:")

        page_helpers.bind_entry(p.entries["intensity_min"], nextE=p.entries["intensity_max"], min_val=0, max_val=1e10, multi=1, ranged=True)
        page_helpers.bind_entry(p.entries["intensity_max"], min_val=0.1, max_val=1e10, multi=1)

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        def display_filtered_scan(main_display, file_path, channel):
            for widget in main_display.winfo_children():
                widget.destroy()

            old_figure = getattr(main_display, "scan_figure", None)

            if old_figure is not None:
                plt.close(old_figure)
            fig = filter_scan.create_filtered_scan_plot(file_path, int(channel))

            mini_display = page_helpers.createFrame(main_display, "mini_display", [0.1, 0.005, 0.8, 0.99], outline=True)

            canvas = FigureCanvasTkAgg(fig, master=mini_display)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            main_display.scan_canvas = canvas
            main_display.scan_figure = fig
        
        p.last_row = page_helpers.createFrame(p, "third_row", [0.35, 0.9, 0.3, 0.05])
        p.Filter = page_helpers.createButton(p.last_row, "Filter", 5, 
                                             lambda: config.update(p.entries, "scan", Scan_Config, nextCall = 
                                                                   lambda: display_filtered_scan(self.panels["mode_display"], data_path, ch)))


    def OpenZoomMenu(self):
        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}
        
        Scan_Data = "/Users/davitmoreno/Downloads/Compressed/config_files/scan.yaml"
        #print("Will add zoom input stuff that will fetch the metadata of file or something...")

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate = False
        p.title = page_helpers.createLabel(p.title_frame, "Zoom Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.6, 0.05])
        p.entries["x_min"], p.entries["x_max"] = page_helpers.createRangeInput(p.first_row, "X:")
        p.second_row = page_helpers.createFrame(p, "second_row", [0.1, 0.19, 0.6, 0.05])
        p.entries["y_min"], p.entries["y_max"] = page_helpers.createRangeInput(p.second_row, "Y:")
    
    def build_mode_ops(self):
        p = self.mode_options
        options_loadout = {
            "run": self.OpenRunMenu,
            "filter": self.OpenFilterMenu,
            "magnification": self.OpenZoomMenu,
        }
        button_size = 0.08

        page_helpers.createToolbar(p, options_loadout, button_size)