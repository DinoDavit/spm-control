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

def createRangeInput(parent, name, min_val = 0, max_val = 100, placeholder_min="min", placeholder_max="max"):
    name = name.rstrip(":")
    vcmd = (parent.register(check.is_num), "%P", name)

    label = createLabel(
        parent,
        text=f"{name}:",
        sz=17,
        font="Arial",
        width=28,
        anchor="e",
        pack=False
    )

    label.pack(side="left", padx=(0, 5), pady=0)

    min_entry = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder_min,
        placeholder_text_color="#b0b0b0",
        width=52,
        height=26,
        font=("Arial", 14),
        justify="center",
        validate="key",
        validatecommand=vcmd
    )
    
    min_entry.bind("<Return>", lambda event: check.within_range(min_entry, min_val, max_val))
    min_entry.bind("<FocusOut>", lambda event: check.within_range(min_entry, min_val, max_val))

    min_entry.pack(side="left", padx=(0, 6), pady=0)

    to_label = createLabel(
        parent,
        text="to",
        sz=15,
        font="Arial",
        width=20,
        pack=False
    )
    to_label.pack(side="left", padx=(0, 6), pady=0)

    max_entry = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder_max,
        placeholder_text_color="#b0b0b0",
        width=52,
        height=26,
        font=("Arial", 14),
        justify="center",
        validate="key",
        validatecommand=vcmd
    )

    max_entry.bind("<Return>", lambda event: check.within_range(max_entry, min_val, max_val))
    max_entry.bind("<FocusOut>", lambda event: check.within_range(max_entry, min_val, max_val))
    
    max_entry.pack(side="left", pady=0)

    return min_entry, max_entry

def createSingleEntry(
    parent,
    name,
    placeholder="value",
    label_width=28,
    entry_width=82,
    min_val=None,
    max_val=None,
    config_key=None,
):
    name = name.rstrip(":")
    config_key = config_key or name

    vcmd = (parent.register(check.is_num), "%P", name)

    label = createLabel(
        parent,
        text=f"{name}:",
        sz=17,
        font="Arial",
        width=label_width,
        anchor="e",
        pack=False,
    )
    label.pack(side="left", padx=(0, 5), pady=0)

    entry = ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        placeholder_text_color="#b0b0b0",
        width=entry_width,
        height=26,
        font=("Arial", 14),
        justify="center",
        validate="key",
        validatecommand=vcmd,
    )
    entry.pack(side="left", pady=0)

    if (min_val or max_val):
        entry.bind("<Return>", lambda event: check.within_range(entry, min_val, max_val))
        entry.bind("<FocusOut>", lambda event: check.within_range(entry, min_val, max_val))

    return entry

def createLabel(
    parent,
    text="",
    sz=18,
    font="Arial",
    side="left",
    x_space=(10, 10),
    y_space=(0, 0),
    expand=False,
    pack=True,
    **kwargs
):
    label = ctk.CTkLabel(
        parent,
        text=text,
        font=(font, sz),
        **kwargs
    )

    if pack:
        label.pack(
            side=side,
            padx=x_space,
            pady=y_space,
            expand=expand
        )

    return label