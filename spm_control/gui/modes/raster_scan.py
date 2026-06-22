import tkinter as tk
import ttkbootstrap as ttk
import sys

def scan():
    print("Hello World")

scan_window = tk.Tk()
scan_window.title('Demo')

title_label = ttk.Label(master = scan_window, text = 'QD Coverslip Scanner', font = 'Calibri 24 bold')

max_width = scan_window.winfo_screenwidth()
max_height = scan_window.winfo_screenheight()

scan_window.geometry(f'{max_width}x{max_height}')

scan_window.mainloop()