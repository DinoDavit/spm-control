import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import yaml

def getDimensions(parent):
    return parent.winfo_screenwidth(), parent.winfo_screenheight()

def addFrame(parent, name, dimensions):
    parent.name = ctk.CTkFrame()
    parent.name.place(
    relx = dimensions[x],
    rely = dimensions[y],
    relwidth = dimensions[width],
    relheight = dimensions[height])

def update_config(updates, file_name):
    with open(file_name, "r") as f:
        doc = yaml.safe_load(f) or {}

    for name, value in updates.items():
        doc[name] = value

    with open(file_name, "w") as f:
        yaml.safe_dump(doc, f, sort_keys=False)
    

def load_required_panels(page, panels, required_panels):
    page.panels = panels
    
    for name in required_panels:
        setattr(page, name, panels[name])

def fillOptions(parent, options, function_calls):
    print("HELLO WORLD")
    
def addButtonDisplay(parent, name, func):
    print("HELLO WROLD")

def addButton(parent, name, func):
    parent.name = ctk.CTkButton(
        master = parent,
        text = name,
        command = func
    )

    parent.name.pack(padx=20, pady=20)

def addCheckbox(parent, name):
    print("HELL OWORLD")


def addRangeInput(parent, name):
        parent.name = ctk.CTkEntry( # might need to do parent.entry[name] have to check since entry might have multiple...
            master=parent, 
            placeholder_text="",
            width=30,
        )

        parent.name.pack(pady=10)
        val = parent.name.get()
        parent.vars[name] = val
        print(parent.vars.items())

def addSingleEntry(parent, name):
    row = ctk.CTkFrame(parent)
    row.pack()

    row.pack_propogate(False)