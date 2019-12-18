
import requests
import json

from library.helpers.generic import is_url

def is_json_url(field_value):

    if is_url(field_value):
        if field_value.endswith(".json"):
            return True
    return False


def get_unique_json_urls_from_schema(schema):
    """
    Get all json urls from a schema, and remove duplicates

    :param schema:
    :return:
    """
    all_json  = [x for x in all_dict_values(schema) if is_json_url(x)]
    return list(set(all_json))


def get_json_as_dict(path_or_url, intent):
    """
    Get json as a dict, either from a url or from a local file path.

    :param path_or_url: a valid url or the path to schema on a local machine
    :intent: a string used to help contextualise any error messages
    :return: dict
    """
    if is_url(path_or_url):
        return get_json_from_http(path_or_url, intent)
    else:
        return get_json_from_local_path(path_or_url, intent)


def get_json_from_local_path(path, intent):
    """
    Load json as dict from a local file path.

    :param path: path to a locally stored json file
    :param intent: a string used to help contextualise any error messages
    :return: dict
    """
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as e:
        raise Exception("Aborting. While attmpeting '{}' we were unable to load "
                        "json from location: '{}'.".format(intent, path)) from e
    return data


def get_json_from_http(url, intent):
    """
    Load json from a provided url, or throw a contextualised exception if we fail

    :param url:      http url
    :param intent:   a short description of why (to inform error messages).
    :return:         dict
    """
    r = requests.get(url)

    if r.status_code != 200:
        raise Exception("While '{}'. Failed to get expected json from endpoint '{}' with status"
                        "code '{}'.".format(intent, url, r.status_code))
    try:
        return r.json()
    except Exception as e:
        raise Exception("While '{}' we were unable to convert the response from '{}' from json to dict"
                        .format(intent, url)) from e


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
