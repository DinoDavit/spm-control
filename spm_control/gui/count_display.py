import customtkinter as ctk

from spm_control.gui.modes import page_helpers
from spm_control.managers.count_manager import CountManager


class Count_Display:
    def __init__(self, app, parent):
        self.app = app
        self.parent = parent
        self.expanded_window = None

        self.ch1_frame = page_helpers.createFrame(
            parent,
            "channel_1",
            [0.05, 0.01, 0.9, 0.32],
            outline=True
        )

        self.ch2_frame = page_helpers.createFrame(
            parent,
            "channel_2",
            [0.05, 0.33, 0.9, 0.32],
            outline=True
        )

        self.ch1_entry, self.ch1_value = page_helpers.createDisplayEntry(
            self.ch1_frame,
            "Channel 1"
        )

        self.ch2_entry, self.ch2_value = page_helpers.createDisplayEntry(
            self.ch2_frame,
            "Channel 2"
        )

        self.expand_button = ctk.CTkButton(
            self.ch1_frame,
            text="⛶",
            width=28,
            height=28,
            corner_radius=5,
            command=self.open_expanded_view
        )

        self.expand_button.place(
            relx=0.98,
            rely=0.05,
            anchor="ne"
        )

        self.expand_button.lift()

        self.count_manager = CountManager(
            app,
            app.hardware_manager,
            update_callback=self.update_counts,
            status_callback=self.update_status,
            interval=0.5
        )

        self.count_manager.start()

    def open_expanded_view(self):
        if self.expanded_window is not None and self.expanded_window.winfo_exists():
            self.expanded_window.lift()
            self.expanded_window.focus()
            return

        self.expanded_window = ctk.CTkToplevel(self.app)
        self.expanded_window.title("Live Counts")
        self.expanded_window.geometry("900x650")
        self.expanded_window.minsize(450, 350)

        self.expanded_window.protocol(
            "WM_DELETE_WINDOW",
            self.close_expanded_view
        )

        self.expanded_ch1_frame = ctk.CTkFrame(
            self.expanded_window
        )

        self.expanded_ch1_frame.place(
            relx=0.05,
            rely=0.05,
            relwidth=0.9,
            relheight=0.4
        )

        self.expanded_ch2_frame = ctk.CTkFrame(
            self.expanded_window
        )

        self.expanded_ch2_frame.place(
            relx=0.05,
            rely=0.55,
            relwidth=0.9,
            relheight=0.4
        )

        self.expanded_ch1_title = ctk.CTkLabel(
            self.expanded_ch1_frame,
            text="Channel 1",
            font=ctk.CTkFont(size=24)
        )

        self.expanded_ch1_title.pack(
            pady=(20, 5)
        )

        self.expanded_ch1_value = ctk.CTkLabel(
            self.expanded_ch1_frame,
            textvariable=self.ch1_value,
            font=ctk.CTkFont(
                size=72,
                weight="bold"
            )
        )

        self.expanded_ch1_value.pack(
            expand=True
        )

        self.expanded_ch2_title = ctk.CTkLabel(
            self.expanded_ch2_frame,
            text="Channel 2",
            font=ctk.CTkFont(size=24)
        )

        self.expanded_ch2_title.pack(
            pady=(20, 5)
        )

        self.expanded_ch2_value = ctk.CTkLabel(
            self.expanded_ch2_frame,
            textvariable=self.ch2_value,
            font=ctk.CTkFont(
                size=72,
                weight="bold"
            )
        )

        self.expanded_ch2_value.pack(
            expand=True
        )

        self.expanded_window.bind(
            "<Configure>",
            self.resize_expanded_text
        )

    def resize_expanded_text(self, event):
        if event.widget is not self.expanded_window:
            return

        reference_size = min(
            event.width,
            event.height
        )

        count_size = max(
            36,
            min(180, int(reference_size * 0.14))
        )

        title_size = max(
            18,
            min(52, int(reference_size * 0.045))
        )

        self.expanded_ch1_title.configure(
            font=ctk.CTkFont(
                size=title_size
            )
        )

        self.expanded_ch2_title.configure(
            font=ctk.CTkFont(
                size=title_size
            )
        )

        self.expanded_ch1_value.configure(
            font=ctk.CTkFont(
                size=count_size,
                weight="bold"
            )
        )

        self.expanded_ch2_value.configure(
            font=ctk.CTkFont(
                size=count_size,
                weight="bold"
            )
        )

    def close_expanded_view(self):
        if self.expanded_window is not None and self.expanded_window.winfo_exists():
            self.expanded_window.destroy()

        self.expanded_window = None

    def update_counts(self, ch1, ch2):
        self.ch1_value.set(
            self.format_count(ch1)
        )

        self.ch2_value.set(
            self.format_count(ch2)
        )

    def update_status(self, status):
        status_messages = {
            "raster_scan": "SCANNING",
            "g2": "G²",
            "tttr": "G²",
            "connecting": "CONNECTING",
            "disconnected": "OFFLINE",
            "error": "ERROR"
        }

        message = status_messages.get(status)

        if message is not None:
            self.ch1_value.set(message)
            self.ch2_value.set(message)

    @staticmethod
    def format_count(count):
        if abs(count) < 10000:
            return str(count)

        coefficient, exponent = f"{count:.2e}".split("e")
        coefficient = coefficient.rstrip("0").rstrip(".")

        return f"{coefficient}e{int(exponent)}"