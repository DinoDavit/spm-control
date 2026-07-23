
from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT
from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk
import time


class Explorer_Page:
    def __init__(self, app):
        required_panels = {
            "mode_options",
            "mode_display",
            "option_parameters",
            "file_display",
        }

        self.panels = app.panels
        page_helpers.reload_panels(self.panels, MAIN_LAYOUT, required_panels, notMain=True)
        time.sleep(0.05)
        page_helpers.load_required_panels(self, self.panels, required_panels)

        self.app = app
        self.OpenFolderMenu()
        self.CreateFileDisplay()

    def OpenFolderMenu(self):
        p = page_helpers.reload_panel(self.panels, MAIN_LAYOUT, "option_parameters")
        p.entries = {}

        p.title_frame = page_helpers.createFrame(p, "title_frame", [0, 0, 1, 0.1], outline=True)
        p.title_frame.pack_propagate(False)
        p.title = page_helpers.createLabel(p.title_frame, "Folder Menu", sz=24, side="top", y_space=(4, 4))

        p.first_row = page_helpers.createFrame(p, "first_row", [0.1, 0.12, 0.7, 0.05])
        p.entries["filter_name"] = page_helpers.createSingleEntry(
            p.first_row, "Filter", numbered_entry=False, placeholder="e.g. g2"
        )

        p.second_row = page_helpers.createFrame(p, "second_row", [0.1, 0.19, 0.7, 0.05])
        p.entries["extension"] = page_helpers.createSingleEntry(
            p.second_row, "Extension", numbered_entry=False, placeholder="e.g. txt"
        )

        page_helpers.bind_entry(p.entries["filter_name"], min_val=None, max_val=None)
        page_helpers.bind_entry(p.entries["extension"], min_val=None, max_val=None, nextE=p.entries["extension"])

        p.last_row = page_helpers.createFrame(p, "third_row", [0.3, 0.8, 0.4, 0.05])
        p.Select_File = page_helpers.createButton(
            p.last_row, "Select File", 5, self.select_and_display_file
        )

    def CreateFileDisplay(self):
        p = self.panels["file_display"]
        p.path_display = page_helpers.createFrame(p, "path_display", [0, 0, 1, 0.5], outline=True)

        p.path_entry = ctk.CTkEntry(p.path_display, placeholder_text="Selected file path", text_color="#67E8F9")
        p.path_entry.pack(fill="both", expand=True, padx=3, pady=3)
        p.path_entry.configure(state="readonly")

    def select_and_display_file(self):
        p = self.panels["option_parameters"]

        filter_name = p.entries["filter_name"].get().strip()
        extension = p.entries["extension"].get().strip().lstrip(".")

        if extension:
            filetypes = [
                (f"{extension.upper()} files", f"*.{extension}"),
                ("All files", "*.*")
            ]
        else:
            filetypes = [("All files", "*.*")]

        selected_file = filedialog.askopenfilename(
            title="Open File",
            filetypes=filetypes
        )

        if not selected_file:
            return

        file_name = Path(selected_file).name

        if filter_name and filter_name.casefold() not in file_name.casefold():
            return

        file_panel = self.panels["file_display"]
        file_panel.path_entry.configure(state="normal")
        file_panel.path_entry.delete(0, "end")
        file_panel.path_entry.insert(0, selected_file)
        file_panel.path_entry.configure(state="readonly")

        display(self.panels["mode_display"], selected_file)


def display(panel, file_path):
    for widget in panel.winfo_children():
        widget.destroy()

    extension = Path(file_path).suffix.lower()

    if extension == ".png":
        mini_display = page_helpers.createFrame(panel, "mini_display", [0.1, 0.005, 0.8, 0.99], outline=True)
        page_helpers.displayImage(mini_display, file_path)
    elif extension == ".txt":
        display_txt(panel, file_path)


def display_txt(panel, file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        content = file.read()

    text_box = ctk.CTkTextbox(panel, wrap="word")
    text_box.pack(fill="both", expand=True)
    text_box.insert("1.0", content)
    text_box.configure(state="disabled")
