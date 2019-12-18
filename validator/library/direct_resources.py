
import requests
from box import BoxList

from library.helpers.json import all_dict_values, get_json_as_dict, is_json_url, get_unique_json_urls_from_schema
from library.helpers.exceptions import exception_as_string, ConfigurationError

def all_http_field_responses_match(validator, schema, **kwargs):

    err_string = "The function 'all_http_field_responses_match' requires a " \
                 "keyword argument of 'status_codes' containing a list of http" \
                 "codes as three digit integers. Got: "

    if "status_codes" not in kwargs.keys():
        raise ConfigurationError(err_string+str(kwargs))

    status_codes_list = kwargs["status_codes"]

    if type(status_codes_list) != list and type(status_codes_list) != BoxList:
        status_codes_list = [status_codes_list]

    if len([x for x in status_codes_list if type(x) != int or x < 200 or x > 600]) > 0:
        raise ConfigurationError(err_string+str(kwargs))

    for field_value in all_dict_values(schema):
        if is_json_url(field_value):
            r = requests.get(field_value)
            if r.status_code not in status_codes_list:
                validator.results.add_result("bad response for {}.".format(field_value),
                            {"status_code_recieved": r.status_code, "codes_allowed": status_codes_list})



def all_referenced_json_documents_load(validator, schema, **kwargs):

    follow_children = False
    if "follow_children" in kwargs:
        follow_children = kwargs["follow_children"]

    all_json_links = get_unique_json_urls_from_schema(schema)

    for json_link in all_json_links:
        try:
            child_schema = get_json_as_dict(json_link, "get json for '{}',".format(json_link))
            if follow_children:
                all_referenced_json_documents_load(validator, child_schema, **kwargs)

        except Exception as e:
            validator.results.add_result("exception encountered for '{}'".format(json_link), exception_as_string(e))



def all_referenced_csv_files_load(validator, schema, **kwargs):

    follow_children = False
    if "follow_children" in kwargs:
        follow_children = kwargs["follow_children"]

    # TODO! - ..it






