import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from spm_control.gui.modes import validators as check

def getDimensions(parent):
    return parent.winfo_screenwidth(), parent.winfo_screenheight()

def load_required_panels(page, panels, required_panels):
    page.panels = panels
    
    for name in required_panels: 
        if name not in panels:
            raise KeyError(f"Required panel '{name}' was not found in app.panels")

        setattr(page, name, panels[name])

def createFrame(parent, name, dimensions):
    debug = False
    if not hasattr(parent, "frames"):
        parent.frames = {}

    if (debug == True):
            col1 ="black"
            col2 = "white"
    else:
        col1 = "transparent"
        col2 = ""

    frame = ctk.CTkFrame(
        parent,
        border_width = 2,
        border_color = col2,
        fg_color = col1,
        width=dimensions[2],
        height=dimensions[3],
    )

    frame.place(
        x=dimensions[0],
        y=dimensions[1],
    )

    parent.frames[name] = frame
    return frame


def createButton(parent, name, func):
    button = ctk.CTkButton(
        master = parent,
        text = name,
        command = func
    )

    button.pack(padx=20, pady=20)

    return button

def createButtonDisplay(parent, func):
    print("HELLO WROLD")

def fillOptions(parent, options, function_calls):
    print("HELLO WORLD")

def createCheckbox(parent, name):
    print("HELL OWORLD")

def createRangeInput(parent, name, placeholder_min="", placeholder_max=""):
    left_paren = ctk.CTkLabel(parent, text="(", font = ("Arial", 25))
    left_paren.pack(side="left", padx=(5, 2))

    min_entry = ctk.CTkEntry(
        master=parent,
        placeholder_text=placeholder_min,
        width=50,
    )
    min_entry.pack(side="left", padx=2, fill="x", expand=True)

    comma = ctk.CTkLabel(parent, text=",", font = ("Arial", 25))
    comma.pack(side="left", padx=2)

    max_entry = ctk.CTkEntry(
        master=parent,
        placeholder_text=placeholder_max,
        width=50,
    )
    max_entry.pack(side="left", padx=2, fill="x", expand=True)

    right_paren = ctk.CTkLabel(parent, text=")", font = ("Arial", 25))
    right_paren.pack(side="left", padx=(2, 5))

    return min_entry, max_entry

def createSingleEntry(parent, name):
    row = ctk.CTkFrame(parent)
    row.pack()

    row.pack_propagate(False)