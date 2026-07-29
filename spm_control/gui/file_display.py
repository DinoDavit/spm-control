from spm_control.gui.modes import page_helpers
import customtkinter as ctk


class FileDisplay:
    def __init__(self, panel):
        self.panel = panel
        self._create_widgets()

    def _create_widgets(self):
        self.path_display = page_helpers.createFrame(
            self.panel,
            "path_display",
            [0, 0, 1, 0.5],
            outline=True
        )

        self.path_entry = ctk.CTkEntry(
            self.path_display,
            placeholder_text="Selected file path",
            text_color="#67E8F9"
        )
        self.path_entry.pack(fill="both", expand=True, padx=3, pady=3)
        self.path_entry.configure(state="readonly")

    def set_path(self, file_path):
        self.path_entry.configure(state="normal")
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, str(file_path))
        self.path_entry.configure(state="readonly")

    def get_path(self):
        return self.path_entry.get().strip()