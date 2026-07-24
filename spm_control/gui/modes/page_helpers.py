from pathlib import Path
import customtkinter as ctk
from PIL import Image
from spm_control.gui.modes import validators as check
from pathlib import Path
from PIL import Image
from tkinter import messagebox


def getDimensions(parent):
    return parent.winfo_screenwidth(), parent.winfo_screenheight()

def createPanels(parent, layout):
    # Getting name from layout and creating corresponding frames
    panels = {}
    for name, dims in layout.items():
        panels[name] = create_panel(parent, name, dims)
    return panels


def create_panel(parent, name, dims):
    x, y, w, h = dims

    panel = ctk.CTkFrame(
        parent,
        border_width=2,
        border_color="white",
        fg_color="black",
        )
    
    panel.place(
        relx=x,
        rely=y,
        relwidth=w,
        relheight=h,
    )

    return panel


def reload_panel(panels, layout, panel_name):
    old_panel = panels[panel_name]
    parent = old_panel.master
    old_panel.destroy()

    new_panel = create_panel(parent, panel_name,layout[panel_name])
    panels[panel_name] = new_panel

    return new_panel


def reload_panels(panels, layout, panel_names, notMain = False):
    """
    Destroy and recreate multiple panels.
    """
    if (notMain == True):
        panel_names.remove("mode_display")
    for panel_name in panel_names:
        reload_panel(panels, layout, panel_name)

    return panels

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

def createToolbar(parent, loadout, button_size, horizontal=True):
    parent.options = {}
    assets = Path(__file__).resolve().parent.parent / "assets"

    for i, (name, command) in enumerate(loadout.items()):
        if (horizontal):
            dims = [button_size * i, 0, button_size, 1]
        else:
            dims = [0, button_size * i, 1, button_size]

        frame = createFrame(
            parent,
            f"{name}_frame",
            dims,
            outline=True,
        )

        button = createButtonDisplay(
            frame,
            str(assets / f"{name}.png"),
            command,
        )

        parent.options[name] = {
            "frame": frame,
            "button": button,
        }

def createButton(parent, name, cRad, func):
    button = ctk.CTkButton(
        master=parent,
        text=name,
        command=func,
        corner_radius=cRad
    )

    button.pack(fill="both", expand=True)

    return button


def createButtonDisplay(parent, PNG, func):
    raw_image = Image.open(PNG).convert("RGBA")

    my_button = ctk.CTkButton(
        master=parent,
        text="",
        command=func,
        fg_color="white",
        hover_color="gray"
    )

    my_button.pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True
    )

    def resize_to_parent(event):
        available_width = event.width
        available_height = event.height

        image_width = int(available_width * 0.6)
        image_height = int(available_height * 0.6)

        btn_image = ctk.CTkImage(
            light_image=raw_image,
            dark_image=raw_image,
            size=(image_width, image_height)
        )

        my_button.configure(image=btn_image)
        my_button.image_ref = btn_image

    parent.bind("<Configure>", resize_to_parent)

    return my_button

# def createCheckbox(parent, text, default=False, side="top"):
#     var = ctk.BooleanVar(value=default)

#     checkbox = ctk.CTkCheckBox(
#         parent,
#         text=text,
#         variable=var
#     )

#     checkbox.pack(side=side, anchor="w", padx=10, pady=5)

#     return checkbox, var

def createRangeInput(parent, name, placeholder_min="min", placeholder_max="max"):
    name = name.rstrip(":")
    vcmd = (parent.register(check.validate_numeric_typing), "%P", name)

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

    min_entry.pack(side="left", padx=(0, 6), pady=0)
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
    multi = 0,
    numbered_entry = True,
):
    name = name.rstrip(":")
    config_key = config_key or name

    if numbered_entry:
        vcmd = (parent.register(check.validate_numeric_typing), "%P", name)
    else:
        vcmd = (parent.register(check.validate_typing), "%P", name)

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

def bind_entry(entry, nextE=None, min_val = 0, max_val = 100, multi=0, ranged=False, emptyOk = False):
    if (min_val or max_val):
            entry.bind("<FocusOut>", lambda event: check.within_range(
                entry, 
                min_val, 
                max_val, 
                multiple = multi, 
                ranged_input=ranged,
                next_entry = nextE,
                EnterKey=False,
                emptyOk = emptyOk),
                )
            
            entry.bind("<Return>", lambda event: check.within_range(
                entry, 
                min_val, 
                max_val, 
                multiple=multi,
                emptyOk = emptyOk),
                )
    else:
        entry.bind("<Return>", lambda event: check.within_range(
                entry, 
                min_val, 
                max_val, 
                multiple=multi,
                emptyOk = emptyOk),
                )

def get_file(panels):
    return panels["file_display"].path_entry.get()

def throwError(message):
    messagebox.showerror("Error", message)

def displayImage(frame, image_source):
    for widget in frame.winfo_children():
        widget.destroy()

    original = Image.open(image_source) if isinstance(image_source, (str, Path)) else image_source.copy()

    label = ctk.CTkLabel(frame, text="")
    label.pack(fill="both", expand=True)

    def resize(event):
        if event.width <= 1 or event.height <= 1:
            return

        image = original.copy()
        image.thumbnail((event.width, event.height))

        ctk_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )

        label.configure(image=ctk_image)
        label.image = ctk_image

    frame.bind("<Configure>", resize)
    frame.after_idle(lambda: resize(
        type("Event", (), {
            "width": frame.winfo_width(),
            "height": frame.winfo_height()
        })()
    ))

    return label

def createDisplayEntry(parent, name, value="0", label_width=90, entry_width=145):
    value_var = ctk.StringVar(value=value)

    label = createLabel(
        parent,
        text=f"{name}:",
        sz=20,
        font="Arial",
        width=label_width,
        anchor="e",
        pack=False
    )
    label.pack(side="left", padx=(0, 8))

    entry = ctk.CTkEntry(
        parent,
        textvariable=value_var,
        width=entry_width,
        height=45,
        font=("Arial", 24, "bold"),
        text_color="red",
        justify="center",
        state="disabled"
    )
    entry.pack(side="left")

    return entry, value_var