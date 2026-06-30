def is_num(raw_value, min_value=None, max_value=None):
    raw_value = raw_value.strip()

    if raw_value == "":
        raise ValueError(f" cannot be empty.")

    try:
        value = float(raw_value)
    except ValueError:
        raise ValueError(f" must be a number.")

    if min_value is not None and value < min_value:
        raise ValueError(f" must be at least {min_value}.")

    if max_value is not None and value > max_value:
        raise ValueError(f" must be at most {max_value}.")

    return value

def is_bool(val):
    if val == "":
        return True

    # allow only booleans
    return val.isboolean()

# def is_withinRange(val, range):
    # try 