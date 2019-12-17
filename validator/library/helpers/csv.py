
import pandas as pd

from library.helpers.generic import is_url

def is_csv_url(field_value):

    if is_url(field_value):
        if field_value.endswith(".csv"):
            return True
    return False


def get_csv_as_pandas(path_or_url, intent):
    """
    Get json as a dict, either from a url or from a local file path.

    :param path_or_url: a valid url or the path to schema on a local machine
    :intent: a string used to help contextualise any error messages
    :return: dict
    """
    try:
        df = pd.read_csv(path_or_url)
        return df
    except Exception as e:
        raise Exception("Aborting. While attmpeting '{}' we were unable to load "
                        "csv into pandas from location: '{}'.".format(intent, path_or_url)) from e

