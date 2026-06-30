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
    )

    frame.place(
        relx=dimensions[0],
        rely=dimensions[1],
        relwidth=dimensions[2],
        relheight=dimensions[3],
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

def createRangeInput(parent, name, placeholder_min="min", placeholder_max="max"):
    vcmd = (parent.register(check.is_num), "%P")
    
    label = ctk.CTkLabel(
        parent,
        text=name,
        font=("Arial", 18)
    )
    label.pack(side="left", padx=(3, 5), expand=True)
    
    left_paren = ctk.CTkLabel(parent, text="(", font = ("Arial", 20.5))
    left_paren.pack(side="left", padx=(4, 1), expand=True)

    min_entry = ctk.CTkEntry(
        master=parent,
        placeholder_text=placeholder_min,
        width=50,
        height=30,
        validatecommand = vcmd
    )
    min_entry.pack(side="left", padx=1, fill="x", expand=True)

    comma = ctk.CTkLabel(parent, text=",", font = ("Arial", 20.5))
    comma.pack(side="left", padx=1)

    max_entry = ctk.CTkEntry(
        master=parent,
        placeholder_text=placeholder_max,
        width=50,
        height=30,
        validatecommand = vcmd
    )
    max_entry.pack(side="left", padx=1, fill="x", expand=True)

    right_paren = ctk.CTkLabel(parent, text=")", font = ("Arial", 20.5))
    right_paren.pack(side="left", padx=(1, 4), expand=True)

    return min_entry, max_entry

def createSingleEntry(parent, name):
    row = ctk.CTkFrame(parent)
    row.pack()

    row.pack_propagate(False)