import tkinter as tk
import ttkbootstrap as ttk
import sys

def scan():
    print("Hello World")

scan_window = tk.Tk()
scan_window.title('Demo')

max_width = scan_window.winfo_screenwidth()
max_height = scan_window.winfo_screenheight()

scan_window.geometry(f'{max_width}x{max_height}')

title_label = ttk.Label(master = scan_window, text = 'QD Coverslip Scanner', font = 'Calibri 24 bold')
title_label.pack()

input_frame = ttk.Frame(master = scan_window, borderwidth=2, relief = 'ridge')
input_frame.pack(side = 'left', fill="both", expand=True)
scan_button = ttk.Button(master = input_frame, text = 'Scan', command = scan)
scan_button.pack(padx = 20, pady = 20)


scan_window.mainloop()