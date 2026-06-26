import customtkinter as ctk
import tkinter as tk
import ttkbootstrap as ttk
import sys
from spm_control.gui.modes import page_helpers


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
        p.vars = {}
        page_helpers.addRangeInput(p, "x")
        page_helpers.addButton(p, "Run", page_helpers.update_config)
