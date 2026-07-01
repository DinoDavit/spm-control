import customtkinter as ctk

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def within_range(entry, min_val, max_val, next_entry = None, multiple = 0):
    raw_val = float(entry.get())
    clamped_val = clamp(raw_val, min_val, max_val)

    if (clamped_val != raw_val):
        entry.delete(0, "end")
        entry.configure(border_color = "red")
        entry.insert(0, str(clamped_val))

    if (multiple and clamped_val % multiple !=0):
        entry.delete(0, "end")
        entry.configure(border_color = "red")
        entry.insert(0, str(round(clamped_val / multiple) * multiple))
    
    else:
        entry.configure(border_color = "green")

        if (next_entry):
            next_entry.focus_set()

        else:
            entry.master.focus_set()

def is_num(raw_value, min_value=None, max_value=None):
    raw_value = raw_value.strip()
    if raw_value != "":
        try:
            value = float(raw_value)
        except ValueError:
            return False
    return True

def is_bool(val):
    if val == "":
        return True

    # allow only booleans
    return val.isboolean()

# def is_withinRange(val, range):
    # try 