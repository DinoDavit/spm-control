import tkinter as tk
import ttkbootstrap as ttk

import sys

def scan():
    print("Hello World")

scan_window = tk.Tk()
scan_window.title('Demo')
scan_window.geometry(f'{max_width}x{max_height}')

title_label = ttk.Label(master = scan_window, text = 'QD Coverslip Scanner', font = 'Calibri 24 bold')
title_label.pack()

observation_frame = ttk.Frame(
    scan_window,
    width = max_width * 0.5,
    height = max_height * 0.5,
    borderwidth = 2,
    relief = 'ridge'
)

input_frame = ttk.Frame(
    scan_window,
    width = max_width*0.2,
    height = max_height * 0.5,
    borderwidth=2, 
    relief = 'ridge')

input_frame.pack(
    side = "bottom",
    anchor = "se",
    padx = 10,
    pady = 10
)
input_frame.pack_propagate(False)




scan_button = ttk.Button(master = input_frame, text = 'Scan', command = scan)
scan_button.pack(padx = 20, pady = 20, side = "bottom")



scan_window.mainloop()