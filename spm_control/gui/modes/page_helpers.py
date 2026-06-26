import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import yaml

def update_config(vars, file_name):
    with open(file_name) as f:
        doc = yaml.load(f)

    for name, val in vars.items():
        doc[name] = val

    with open('file_to_edit.yaml', 'w') as f:
        yaml.dump(doc, f)
    

def load_required_panels(page, panels, required_panels):
    page.panels = panels

    print(panels)
    
    for name in required_panels:
        setattr(page, name, panels[name])

def fillOptions(parent, options, function_calls):
    print("HELLO WORLD")
    
def addButton(parent, name, func):
    parent.button = ctk.CTkButton(
        master = parent,
        text = name,
        command = func
    )

    parent.button.pack(padx=20, pady=20)

def addCheckbox(parent, name):
    print("HELL OWORLD")


def addRangeInput(parent, name):
        parent.entry = ctk.CTkEntry( # might need to do parent.entry[name] have to check since entry might have multiple...
            master=parent, 
            placeholder_text="",
            width=30,
        )

        parent.entry.pack(pady=10)
        val = parent.entry.get()
        parent.vars[name] = val

def addSingleEntry(parent, name):
    row = ctk.CTkFrame(parent)
    row.pack()

    row.pack_propogate(False)