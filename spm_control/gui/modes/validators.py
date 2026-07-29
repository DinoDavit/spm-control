import customtkinter as ctk
import re


def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def within_range(
    entry,
    min_val,
    max_val,
    next_entry=None,
    multiple=0,
    EnterKey=True,
    ranged_input=False,
    emptyOk=False
):
    value = entry.get().strip()

    if is_empty(value):
        if emptyOk:
            entry.configure(border_color="green")
        else:
            entry.configure(border_color="red")

        return False

    if min_val is None and max_val is None:
        entry.configure(border_color="green")

        if EnterKey:
            if next_entry is not None:
                next_entry.focus_set()
            else:
                entry.master.focus_set()

        return True

    try:
        raw_val = float(value)
    except ValueError:
        entry.configure(border_color="red")
        return False

    if ranged_input and next_entry is not None:
        next_value = next_entry.get().strip()

        if not is_empty(next_value):
            try:
                raw_val2 = float(next_value)
            except ValueError:
                next_entry.configure(border_color="red")
                return False

            max_val = min(max_val, raw_val2)

    clamped_val = clamp(raw_val, min_val, max_val)

    if clamped_val != raw_val:
        entry.delete(0, "end")
        entry.insert(0, str(clamped_val))
        entry.configure(border_color="red")
        return False

    if multiple and clamped_val % multiple != 0:
        rounded_val = round(clamped_val / multiple) * multiple

        entry.delete(0, "end")
        entry.insert(0, str(rounded_val))
        entry.configure(border_color="red")
        return False

    entry.configure(border_color="green")

    if EnterKey:
        if next_entry is not None:
            next_entry.focus_set()
        else:
            entry.master.focus_set()

    return True

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

def validate_typing(proposed_value, typed_char):
    if proposed_value == "":
        return True

    return True