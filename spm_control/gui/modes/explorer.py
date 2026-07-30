from pathlib import Path
from tkinter import filedialog

from spm_control.gui.modes import page_helpers
from spm_control.gui.layout import MAIN_LAYOUT


class Explorer_Page:
    def __init__(self, app):
        required_panels = {
            "mode_options",
            "mode_display",
            "option_parameters",
        }

        self.app = app
        self.panels = app.panels

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

        self.OpenFolderMenu()

    def OpenFolderMenu(self):
        p = page_helpers.reload_panel(
            self.panels,
            MAIN_LAYOUT,
            "option_parameters"
        )

        p.entries = {}

        p.title_frame = page_helpers.createFrame(
            p,
            "title_frame",
            [0, 0, 1, 0.1],
            outline=True
        )
        p.title_frame.pack_propagate(False)

        p.title = page_helpers.createLabel(
            p.title_frame,
            "Folder Menu",
            sz=24,
            side="top",
            y_space=(4, 4)
        )

        p.first_row = page_helpers.createFrame(
            p,
            "first_row",
            [0.1, 0.12, 0.7, 0.05]
        )
        p.entries["filter_name"] = page_helpers.createSingleEntry(
            p.first_row,
            "Filter",
            numbered_entry=False,
            placeholder="e.g. g2"
        )

        p.second_row = page_helpers.createFrame(
            p,
            "second_row",
            [0.1, 0.19, 0.7, 0.05]
        )
        p.entries["extension"] = page_helpers.createSingleEntry(
            p.second_row,
            "Extension",
            numbered_entry=False,
            placeholder="e.g. txt"
        )

        page_helpers.bind_entry(
            p.entries["filter_name"],
            min_val=None,
            max_val=None
        )

        page_helpers.bind_entry(
            p.entries["extension"],
            min_val=None,
            max_val=None
        )

        p.last_row = page_helpers.createFrame(
            p,
            "third_row",
            [0.35, 0.9, 0.3, 0.05]
        )

        p.select_file = page_helpers.createButton(
            p.last_row,
            "Select File",
            5,
            self.select_and_display_file
        )

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

        if (
            filter_name
            and filter_name.casefold() not in file_name.casefold()
        ):
            page_helpers.throwError(
                f"Selected file does not contain '{filter_name}'."
            )
            return

        try:
            self.app.file_display.set_path(selected_file)
            self.app.main_display.display_selected_file(selected_file)
            print("Selected file:", selected_file)

        except Exception as error:
            page_helpers.throwError(str(error))