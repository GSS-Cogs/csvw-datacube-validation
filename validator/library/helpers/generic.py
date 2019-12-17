
def is_url(field_value):
    """Is a given path a url or a local file path"""

    if not isinstance(field_value, str):
        return False

    if "http" in field_value or "https" in field_value:
        if "//" in field_value:
            return True
    return False