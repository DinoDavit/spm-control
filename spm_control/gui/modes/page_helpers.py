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

def createFrame(parent, name, dimensions, outline = False):
    debug = False
    if not hasattr(parent, "frames"):
        parent.frames = {}

    if (debug == True):
            col1 ="black"
            col2 = "white"
    else:
        col1 = "transparent"
        col2 = ""

    if (outline == True):
        col1 ="black"
        col2 = "white"

    frame = ctk.CTkFrame(
        parent,
        border_width = 2,
        border_color = col2,
        fg_color = col1,
    )


    # Using relative coordinates because those scale
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

    button.pack(padx=20, pady=20, expand = True)

    return button

def createButtonDisplay(parent, func):
    print("HELLO WROLD")

def fillOptions(parent, options, function_calls):
    print("HELLO WORLD")

def createCheckbox(parent, name):
    print("HELL OWORLD")

def createRangeInput(parent, name, placeholder_min="min", placeholder_max="max"):
    vcmd = (parent.register(check.is_num), "%P")

    name = name.rstrip(":")  # prevents x::

    label = ctk.CTkLabel(
        parent,
        text=f"{name}:",
        font=("Arial", 17, "bold"),
        width=28,
        anchor="e"
    )
    label.pack(side="left", padx=(0, 5))

    min_entry = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder_min,
        placeholder_text_color="#b0b0b0",
        width=52,
        height=26,
        font=("Arial", 14),
        validate="key",
        validatecommand=vcmd
    )
    min_entry.pack(side="left", padx=(0, 5))

    to_label = ctk.CTkLabel(
        parent,
        text="to",
        font=("Arial", 16),
        width=20
    )
    to_label.pack(side="left", padx=(0, 5))

    max_entry = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder_max,
        placeholder_text_color="#b0b0b0",
        width=52,
        height=26,
        font=("Arial", 14),
        validate="key",
        validatecommand=vcmd
    )
    max_entry.pack(side="left")

    return min_entry, max_entry

def createSingleEntry(parent, name):
    row = ctk.CTkFrame(parent)
    row.pack()

    row.pack_propagate(False)


def createLabel(parent, text="", sz = 18, font = "Arial", side = "left", x_space = (10, 10), y_space = (0, 0), scale = True, expand = False):
    label = ctk.CTkLabel(
    parent,
    text=text,
    font = (font, sz),
    )
    label.pack(side=side, padx=x_space, pady=y_space, expand=expand)

    return label