import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk

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
        text = 'Name',
        command = func
    )

    parent.button.pack(padx=20, pady=20)

def addCheckbox(parent, name):
    print("HELL OWORLD")


def add_range_input(parent, name):
        parent.my_entry = ctk.CTkEntry(
            master=parent, 
            placeholder_text="",
            width=30,
        )
        parent.my_entry.pack(pady=10)

        parent.my_entry = ctk.CTkEntry(
            master=parent, 
            placeholder_text="",
            width=30
        )
        parent.my_entry.pack(padx=1)

def add_single_entry(parent, name):
    row = ctk.CTkFrame(parent)
    row.pack()

    row.pack_propogate(False)


