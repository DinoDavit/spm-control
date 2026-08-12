import yaml
import re


def parse_config_value(raw_value, emptyOk=False, placeholder=None):
    # Getting raw value
    raw_value = raw_value.strip()

    if not raw_value and emptyOk:
        # Not sure why placeholder not in "None"
        raw_value = str(placeholder).strip() if placeholder not in (None, "") else ""

    # Boolean
    if raw_value.lower() == "true":
        return True
    if raw_value.lower() == "false":
        return False

    # Integer: 50, -50, using regex because easier
    if re.fullmatch(r"-?\d+", raw_value):
        return int(raw_value)

    # Float: 50.5, -50.5, .5, 50., 1e5, -1e5
    if re.fullmatch(r"-?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?", raw_value):
        return float(raw_value)

    # Otherwise keep as string
    return raw_value


def update(updates, branch_name, file_name, nextCall = None, emptyOk=False):
    # Opens the yaml file if there is one provided
    with open(file_name, "r") as f:
        doc = yaml.safe_load(f) or {}

    # Unecessary?
    if branch_name not in doc:
        doc[branch_name] = {}

    # Looks at name and entries in items which are widgets
    for name, entry in updates.items():
        raw_value = entry.get()
        placeholder = None

        # If it is empty, simply get's placeholder text in customtkinter widget
        if not raw_value.strip() and emptyOk:
            try:
                placeholder = entry.cget("placeholder_text")
            except (AttributeError, ValueError):
                pass

        # Tries parsing the element
        element = parse_config_value(raw_value, emptyOk=emptyOk, placeholder=placeholder)
        doc[branch_name][name] = element

    # Opening the yaml file safely
    # Unecessary sort_keys argument and f?
    with open(file_name, "w") as f:
        yaml.safe_dump(doc, f, sort_keys=False)
        
    # In case there is a nextCall after config values updated, like measuring
    if (nextCall is not None):
        nextCall()


# Same principle as above method except now just checks selection
# Selection has format (TRUE/FALSE, command)
def update_selection(selection, branch_name, file_name, nextCall=None):
    with open(file_name, "r") as f:
        doc = yaml.safe_load(f) or {}

    if branch_name not in doc:
        doc[branch_name] = {}

    for name, value in selection.items():
        doc[branch_name][name] = value

    with open(file_name, "w") as f:
        yaml.safe_dump(doc, f, sort_keys=False)

    if nextCall is not None:
        nextCall()