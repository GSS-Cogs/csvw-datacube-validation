
import re

from box import Box

from validator.helpers.reference import get_cogs_implied_resources
from validator.helpers.pandas import assertions
from validator.helpers.csv import get_csv_as_pandas
from validator.cacher import cache

def validate_columns_csvs_for_reference_repos_used_by_schema(validator, schema, **kwargs):
    """
    Validates a csv file used for columns reference data

    :param validator:
    :param schema:
    :param kwargs:
    :return:
    """

    paths_to_columns_files = [x for x in get_cogs_implied_resources(schema, validator.local_ref) if x.endswith("columns.csv")]

    for path in paths_to_columns_files:
        validate_columns_csv(validator, path)


@cache
def validate_columns_csv(validator, path):
    """

    :param validator:
    :param csv_path:
    :return:
    """
    df = get_csv_as_pandas(path, "get column csv '{}' for validation.".format(path))

    patterns = [
        Box({
            "column": "value_template",
            "begins_with": "http://gss-data.org.uk/def/concept/",
            "but_doesnt_end_with": "[A-Za-z0-9-]+\/{[A-Za-z0-9_]*}$",
            "example": "http://gss-data.org.uk/def/concept/styled-like-this/{styled_like_this}"
            }),
        Box({
            "column": "property_template",
            "begins_with": "http://gss-data.org.uk/def/dimension/",
            "but_doesnt_end_with": "[A-Za-z0-9-]*$",
            "example": "http://gss-data.org.uk/def/dimension/styled-like-this"
            }),
        Box({
            "column": "value_template",
            "begins_with": "http://gss-data.org.uk/def/measure/",
            "but_doesnt_end_with": "{[A-Za-z0-9_]*}$",
            "example": "http://gss-data.org.uk/def/measure/{styled_like_this}"
            })
        ]

    for p in patterns:

        finder = assertions.begins_then_not_re(p.begins_with, p.but_doesnt_end_with)
        badly_formatted_cells = list(df[p.column][df[p.column].apply(finder) == True].unique())
        for cell_val in badly_formatted_cells:
            validator.results.add_result("The path segment '{}' in column '{}' is incorrectly formatted."
                                    .format(cell_val[len(p.begins_with):], p.column),
                                    {"got": cell_val, "correct (example):": p.example,
                                    "path": path})

    # Confirm 'name' formatting
    pattern = re.compile("[a-z0-9_]")
    for name in list(df["name"].unique()):
        if pattern.match(name) == None:
            validator.results.add_result("The name '{}' in column file '{}' is malformed.".format(name, path),
                                        {"got": name, "should_be": "lower case letters and hyphens only"})


