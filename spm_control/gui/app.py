import ttkbootstrap as ttk
import customtkinter as ctk



def main():
    app = Application()
    app.mainloop()


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SPM App")

        max_width = self.winfo_screenwidth()
        max_height = self.winfo_screenheight()
        self.geometry(f"{max_width}x{max_height}")

# # build frames/pages here

# app.mainloop()

if __name__ == "__main__":
    main()