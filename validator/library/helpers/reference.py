
from library.helpers.json import all_dict_values

def get_cogs_implied_resources(schema):
    """
    A very cogs specific function. Given a csvw resource, what unspecified csv
    resources can we indfer

    :param schema:
    :return: list of csv and json links
    """

    # ------------------------------------------------
    # Get resources based on provided schema locations

    expected_items = [
        "columns.csv",
        "components.csv",
    ]

    all_string_schema_fields = [x for x in all_dict_values(schema) if isinstance(x, str)]

    implied_resources = []
    for field in all_string_schema_fields:
        if "codelist-schema.json" in field:
            for expected_item in expected_items:
                new_field = field.replace("codelist-schema.json", expected_item)
                implied_resources.append(new_field)

    # TODO - move to above loop once we're happy this is solid
    # -----------------------------------------
    # Get resources based on provided scv paths

    for field in all_string_schema_fields:

        # Old style
        if "https://gss-cogs.github.io/ref" in field and "/codelists" in field:
            ref_repo = field.split("/codelists")[0].split("/")[-1]

            for expected_item in expected_items:
                resource_path = "https://gss-cogs.github.io/" + ref_repo + "/" + expected_item
                implied_resources.append(resource_path)

        # New style
        if "https://gss-cogs.github.io/family" in field and '/reference/codelists/' in field:
            ref_repo = field.split("/reference/codelists")[0].split("/")[-1]

            for expected_item in expected_items:
                resource_path = "https://gss-cogs.github.io/" + ref_repo + "/reference/" + expected_item
                implied_resources.append(resource_path)


    # Get rid of all duplicates
    unique_implied_resources = list(set(implied_resources))

    return unique_implied_resources