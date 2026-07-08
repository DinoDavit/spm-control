import customtkinter as ctk
import re


def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def within_range(entry, min_val, max_val, next_entry = None, multiple = 0, EnterKey=True, ranged_input=False):
    raw_val = float(entry.get())

    if (ranged_input and not is_empty(next_entry.get())):
        raw_val2 = float(next_entry.get())
        min_val = min(min_val, raw_val2)
    clamped_val = clamp(raw_val, min_val, max_val)

    if (clamped_val != raw_val):
        entry.delete(0, "end")
        entry.configure(border_color = "red")
        entry.insert(0, str(clamped_val))

    elif (multiple and clamped_val % multiple !=0 and str(clamped_val)[-2:]!=".0"):
        entry.delete(0, "end")
        entry.configure(border_color = "red")
        entry.insert(0, str(round(clamped_val / multiple) * multiple))
    
    else:
        entry.configure(border_color = "green")

        if (next_entry):
            next_entry.focus_set()

        elif(EnterKey):
            entry.master.focus_set()

def is_empty(raw_val):
    return raw_val==""

def is_num(raw_value, min_value=None, max_value=None):
    raw_value = raw_value.strip()
    if raw_value != "":
        try:
            value = float(raw_value)
        except ValueError:
            return False
    return True

def validate_numeric_typing(proposed_value, typed_char):
    if proposed_value == "":
        return True

    allowed_chars = "0123456789.-eE"

    return all(char in allowed_chars for char in proposed_value)

def is_bool(val):
    if val == "":
        return True

    # allow only booleans
    return val.isboolean()