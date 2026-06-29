import yaml
import re

def parse_config_value(raw_value):
    # Because value is correct from the validators.py
    # This funciton could be a general return
    raw_value = raw_value.strip()

    # Boolean
    if raw_value.lower() == "true":
        return True
    if raw_value.lower() == "false":
        return False

    # Integer: 50, -50
    if re.fullmatch(r"-?\d+", raw_value):
        return int(raw_value)

    # Float: 50.5, -50.5, .5, 50.
    if re.fullmatch(r"-?(\d+\.\d*|\.\d+)", raw_value):
        return float(raw_value)

    # Otherwise keep as string
    return raw_value


def update(updates, branch_name, file_name):
    with open(file_name, "r") as f:
        doc = yaml.safe_load(f) or {}

    for name, entry in updates.items():
        element = parse_config_value(entry.get())
        doc[branch_name][name] = element

    with open(file_name, "w") as f:
        yaml.safe_dump(doc, f, sort_keys=False)