import customtkinter as ctk
import tkinter as tk
import ttkbootstrap as ttk
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

        page_helpers.load_required_panels(
            self, self.panels, required_panels)

        self.app = app
        self.build_display()
        self.build_main_ops()

    def build_display(self):
        title = ctk.CTkLabel(
            master=self.mode_display, 
            text="Main Scan Display", 
            font=("Arial", 16, "bold"),
        text_color="white",)

        title.pack(padx=10, pady=10)
    
    def build_main_ops(self):
        p = self.option_parameters # main panel/parent
        p.entries = {}
        # Storing them in dictionary to later access them all in yaml file under same name
        Scan_Config = "/Users/davitmoreno/Downloads/Compressed/config_files/scan.yaml"
        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.1, 0.6, 0.05])
        p.entries["x"] = page_helpers.createRangeInput(p.first_row, "x:")
        p.second_row = page_helpers.createFrame(p, "second_row", [0.1, 0.16, 0.6, 0.05])
        p.entries["y"] = page_helpers.createRangeInput(p.second_row, "y:")


        p.Run = page_helpers.createButton(p, "Run", lambda: config.update(p.entries, "scan", Scan_Config))

