
from library.helpers.json import all_dict_values

def get_cogs_implied_resources(schema):
    """
    A very cogs specific function. Given a csvw resource, what unspecified csv
    resources can we indfer

    :param schema:
    :return: list of csv and json links
    """
    replacers = [
        {"codelist-schema.json": "columns.csv"},
        {"codelist-schema.json": "components.csv"},
        {"codelist-schema.json": "columns.csv-metadata.json"},
        {"codelist-schema.json": "components.csv-metadata.json"}
    ]

    all_string_schema_fields = [x for x in all_dict_values(schema) if isinstance(x, str)]

    print(all_string_schema_fields)

    implied_resources = []
    for field in all_string_schema_fields:
        for replacer in replacers:
            for old_string, new_string in replacer.items():
                if old_string in field:
                    new_field = field.replace(old_string, new_string)
                    implied_resources.append(new_field)

    unique_implied_resources = list(set(implied_resources))

    return unique_implied_resources