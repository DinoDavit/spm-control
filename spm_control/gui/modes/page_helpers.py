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
    if not hasattr(parent, "frames"):
        parent.frames = {}

    frame = ctk.CTkFrame(
        parent,
        border_width = 2,
        border_color = "white",
        fg_color = "black",
    )

    frame.place(
        relx=dimensions["x"],
        rely=dimensions["y"],
        relwidth=dimensions["width"],
        relheight=dimensions["height"],
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

def createRangeInput(parent, name, placeholder = ""):
        RangeInput = ctk.CTkEntry( # might need to do parent.entry[name] have to check since entry might have multiple...
            master=parent, 
            placeholder_text=placeholder,
            width=30,
            
        )

        RangeInput.pack(pady=10)
        return RangeInput

def createSingleEntry(parent, name):
    row = ctk.CTkFrame(parent)
    row.pack()

    row.pack_propogate(False)