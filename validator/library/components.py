
from box import Box

from validator.helpers.reference import get_cogs_implied_resources
from validator.helpers.pandas import assertions
from validator.helpers.csv import get_csv_as_pandas
from validator.cacher import cache

def validate_components_csvs_for_reference_repos_used_by_schema(validator, schema, **kwargs):
    """
    Validates a csv file used for columns reference data

    :param validator:
    :param schema:
    :param kwargs:
    :return:
    """

    paths_to_components_files = [x for x in get_cogs_implied_resources(schema, validator.local_ref) if x.endswith("components.csv")]

    for path in paths_to_components_files:
        validate_components_csv(validator, path)


@cache
def validate_components_csv(validator, path):
    """

    :param validator:
    :param csv_path:
    :return:
    """
    df = get_csv_as_pandas(path, "get components csv '{}' for validation.".format(path))

    patterns = [
        Box({
            "column": "Codelist",
            "begins_with": "http://gss-data.org.uk/def/concept-scheme/",
            "but_doesnt_end_with": "[A-Za-z0-9-]*$",
            "example": "http://gss-data.org.uk/def/concept-scheme/styled-like-this"
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