import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import yaml

def getDimensions(parent):
    return parent.winfo_screenwidth(), parent.winfo_screenheight()

def createFrame(parent, name, dimensions):
    frame = ctk.CTkFrame(parent)

    frame.place(
        relx=dimensions["x"],
        rely=dimensions["y"],
        relwidth=dimensions["width"],
        relheight=dimensions["height"],
    )

    parent.frames[name] = frame

    return frame

def update_config(updates, name, file_name):
    with open(file_name, "r") as f:
        doc = yaml.safe_load(f) or {}

    for value in updates.items():
        doc[name] = value

    with open(file_name, "w") as f:
        yaml.safe_dump(doc, f, sort_keys=False)
    

def load_required_panels(page, panels, required_panels):
    page.panels = panels
    
    for name in required_panels:
        if name not in panels:
            raise KeyError(f"Required panel '{name}' was not found in app.panels")

        setattr(page, name, panels[name])

def fillOptions(parent, options, function_calls):
    print("HELLO WORLD")
    
def createButtonDisplay(parent, func):
    print("HELLO WROLD")

def createButton(parent, name, func):
    button = ctk.CTkButton(
        master = parent,
        text = name,
        command = func
    )

    button.pack(padx=20, pady=20)

    return button

def createCheckbox(parent, name):
    print("HELL OWORLD")


def createRangeInput(parent, name, placeholder = ""):
        RangeInput = ctk.CTkEntry( # might need to do parent.entry[name] have to check since entry might have multiple...
            master=parent, 
            placeholder_text=placeholder,
            width=30,
        )

        val = RangeInput.get()
        parent.vars[name] = val
        RangeInput.pack(pady=10)
        return RangeInput

def createSingleEntry(parent, name):
    row = ctk.CTkFrame(parent)
    row.pack()

    row.pack_propogate(False)