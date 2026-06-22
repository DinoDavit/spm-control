import ttkbootstrap as ttk


def main():
    app = ttk.Window(themename="superhero")
    app.title("SPM Control Workbench")

    max_width = app.winfo_screenwidth()
    max_height = app.winfo_screenheight()


    app.geometry(f"{max_width}x{max_height}")

    # build frames/pages here

    app.mainloop()


if __name__ == "__main__":
    main()