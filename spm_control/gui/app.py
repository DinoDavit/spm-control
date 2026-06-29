from spm_control.gui.modes.raster_scan import Scan_Page
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

layout = {
    # Creating a main layout of dimensions for main panels
    # These main panels should remain roughly the same despite mode
    "settings": (0, 0, 0.06, 0.1),
    "modes": (0, 0.1, 0.06, 0.8),
    "mode_options": (0.06, 0, 0.744, 0.1),
    "mode_display": (0.06, 0.1, 0.744, 0.8),
    "option_parameters": (0.805, 0.1, 0.19, 0.6),
    "counts": (0.805, 0.7, 0.19,0.3),
}

class Application(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("SPM App")

        # Getting max dimensions of monitor
        max_width = self.winfo_screenwidth()
        max_height = self.winfo_screenheight()

        self.geometry(f"{max_width}x{max_height}")

        self.panels = {}
        # Getting name from layout and creating corresponding frames
        for name, (x, y, width, height) in layout.items():

            self.panels[name] = ctk.CTkFrame(
                self,
                border_width = 2,
                border_color = "white",
                fg_color = "black",
            )

            # Defining placement and dimensions of frames
            self.panels[name].place(
                relx = x,
                rely = y,
                relwidth = width,
                relheight = height,
            )

        self.raster_scan_page = Scan_Page(self)
        

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()