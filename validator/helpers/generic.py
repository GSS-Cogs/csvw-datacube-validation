
def localise(links, local_ref):
    """
    Give a bunch of links, localise them

    :param schem:
    :return:
    """

    # Where we are using local reference sources, substitute paths appropriately
    if local_ref == {}:
        return links # that was easy!
    else:
        localised_list = []
        for link in links:
            for k, v in local_ref.items():
                found = False
                if k in link:
                    localised_resource = v+link.split(k)[1]
                    localised_list.append(localised_resource)
                    found = True
                    break
            if not found:
                localised_list.append(link)

    return localised_list


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