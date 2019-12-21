
def is_url(field_value):
    """Is a given path a url or a local file path"""

    if not isinstance(field_value, str):
        return False

    if "http" in field_value or "https" in field_value:
        if "//" in field_value:
            return True
    return False


def all_dict_values(input):
    """Helper function to get all field values within a dictionary"""
    output = []
    if type(input) == dict:
        for _, v in input.items():
            output += all_dict_values(v)
    elif type(input) == list:
        for v in input:
            output += all_dict_values(v)
    else:
        output.append(input)
    return output