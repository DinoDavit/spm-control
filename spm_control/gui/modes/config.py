import yaml
import re


def parse_config_value(raw_value, emptyOk=False, placeholder=None):
    raw_value = raw_value.strip()

    if not raw_value and emptyOk:
        raw_value = str(placeholder).strip() if placeholder not in (None, "") else ""

    # Boolean
    if raw_value.lower() == "true":
        return True
    if raw_value.lower() == "false":
        return False

    # Integer: 50, -50
    if re.fullmatch(r"-?\d+", raw_value):
        return int(raw_value)

    # Float: 50.5, -50.5, .5, 50., 1e5, -1e5
    if re.fullmatch(r"-?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?", raw_value):
        return float(raw_value)

    # Otherwise keep as string
    return raw_value


def update(updates, branch_name, file_name, nextCall = None, emptyOk=False):
    with open(file_name, "r") as f:
        doc = yaml.safe_load(f) or {}

    if branch_name not in doc:
        doc[branch_name] = {}

    for name, entry in updates.items():
        raw_value = entry.get()
        placeholder = None

        if not raw_value.strip() and emptyOk:
            try:
                placeholder = entry.cget("placeholder_text")
            except (AttributeError, ValueError):
                pass

        element = parse_config_value(raw_value, emptyOk=emptyOk, placeholder=placeholder)
        doc[branch_name][name] = element

    with open(file_name, "w") as f:
        yaml.safe_dump(doc, f, sort_keys=False)
        
    if (nextCall is not None):
        nextCall()


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