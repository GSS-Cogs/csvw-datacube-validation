
from library.helpers.generic import is_url
from library.helpers.exceptions import BadReferalError, ReferenceError

def get_obs_path_from_schema(schema, schema_path):
    """
    Given a schema_url and the schema as a dict, confirm that the observation file
    exists and is reachable at the specified place.

    :param schema_path:
    :param schema:
    :return: obs_path
    """

    # The obervations file will be defined by a
    not_http = [x for x in schema["tables"] if type(x["tableSchema"]) != str]
    if len(not_http) != 1:
        raise BadReferalError("Unable to determine the observation file from the information provided "
                         "by csvm schema '{}'.")

    obs_file_name = not_http[0]["url"]
    return "/".join(schema_path.split("/")[:-1])+"/"+obs_file_name



def get_obs_file_table_schema(schema):
    """
    Give a csvw identify the tableschema that defines our observation csv

    :param schema: schema as dict
    :return: schema.tableSchema (for the obs file) as dict
    """

    identified_tableSchemas = []
    for table in [x for x in schema["tables"] if "url" in x.keys()]:
        if not is_url(table["url"]):
            identified_tableSchemas.append(table)

    if len(identified_tableSchemas) == 0:
        raise ReferenceError("Could not identify the tableschema for the observation file")

    if len(identified_tableSchemas) > 1:
        raise ReferenceError("Could not uniquely identify the tableschema for the observation file")

    return identified_tableSchemas[0]