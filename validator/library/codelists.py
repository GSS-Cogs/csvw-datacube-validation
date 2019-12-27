
import re

from validator.helpers.reference import get_all_codelist_paths_for_schema
from validator.helpers.csv import get_csv_as_pandas
from validator.cacher import cache

def validate_codelist_csvs_for_reference_repos_used_by_schema(validator, schema, **kwargs):
    """
    Validates a csv file used for columns reference data

    :param validator:
    :param schema:
    :param kwargs:
    :return:
    """

    paths_to_codelist_files = [x for x in get_all_codelist_paths_for_schema(schema, validator.local_ref) if x.endswith(".csv")]

    for path in paths_to_codelist_files:
        validate_codelist_csv(validator, path)

@cache
def validate_codelist_csv(validator, path):

    df = get_csv_as_pandas(path, "get column csv '{}' for validation.".format(path))

    # -----------
    # Notation

    notation_pattern = re.compile("[a-z0-9-]")
    notation_key = "notation" if "notation" in df.columns.values else "Notation"
    all_notations = df[notation_key].unique()

    # Basic pattern re
    malformed_notations = [x for x in all_notations if not notation_pattern.match(x)]
    if len(malformed_notations) != 0:
        validator.results.add_result("values in the notation column of '{}' should be "
                                     "lowercase letters, numbers and hyphens only"
                                     .format(path), {"incorrect": malformed_notations})

    # -----------
    # Sort Priority
    # TODO - reactor, there's no way it should be this long
    sort_key = "Sort Priority" if "Sort Priority" in df.columns.values else "sort priority"

    not_nans = [x for x in list(df[sort_key]) if str(x) != "" and str(x) != "nan"]
    int_sort_fields = [int(x) for x in not_nans]
    len_int_sort_fields = len(int_sort_fields)

    blank_sort_fields = [x for x in list(df[sort_key]) if str(x) == "" or str(x) == "nan"]
    len_blank_sort_fields = len(blank_sort_fields)

    # If we've no integers, we should have a blank on every row
    if len_int_sort_fields == 0:
        if len(df) != len_blank_sort_fields:
            validator.results.add_result("The sort priority field in '{}' should only contain"
                                         "integers or all blank cells.".format(path),
                                         {"integer cells": len_int_sort_fields,
                                          "blank cells": len_blank_sort_fields,
                                          "total cells": len(df)})

    # if we have integers, make sure we have one for every line
    if len_int_sort_fields > 0:
        if df[sort_key].dtype != int:
            validator.results.add_result("The sort priority field in '{}' is malformed."
                                         " If we are using Sort Priority, we should have"
                                         " an integer on every line.".format(path),
                                         {})  # TODO - it'd be nice to lists the non int's
        else:
            # If we do, make sure there's an order to them
            order = set(int_sort_fields)
            for i in range(1, len(order) + 1):
                if i not in int_sort_fields:
                    validator.results.add_result("The sort priority field in '{}' is malformed."
                                                 " If we are using Sort Priority, the integers"
                                                 " should follow a sequence incrementing in 1's."
                                                 .format(path), {"sequence": order})
                    break

