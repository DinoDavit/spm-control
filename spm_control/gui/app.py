import ttkbootstrap as ttk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

layout = {
    "save_file": (0, 0, 0.06, 0.1),
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

        max_width = self.winfo_screenwidth()
        max_height = self.winfo_screenheight()
        self.geometry(f"{max_width}x{max_height}")

        for name, (x, y, width, height) in layout.items():
            self.frame = ctk.CTkFrame(
                self,
                border_width = 2,
                border_color = "white",
                fg_color = "black",
            )
        
            self.frame.place(
                relx = x,
                rely = y,
                relwidth = width,
                relheight = height,
            )

        # Building the 3x3 frames that will be used

        
        # self.top_left = ctk.CTkFrame(self, border_width=2)
        # self.top_center = ctk.CTkFrame(self, border_width=2)
        # self.top_right = ctk.CTkFrame(self, border_width=2)

        # self.left = ctk.CTkFrame(self, border_width=2)
        # self.center = ctk.CTkFrame(self, border_width=2)
        # self.right = ctk.CTkFrame(self, border_width=2)

        # self.bottom_left = ctk.CTkFrame(self, border_width=2)
        # self.bottom_center = ctk.CTkFrame(self, border_width=2)
        # self.bottom_right = ctk.CTkFrame(self, border_width=2)


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()