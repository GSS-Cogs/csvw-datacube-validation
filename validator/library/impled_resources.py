
import re

from box import Box

from validator.helpers.reference import get_cogs_implied_resources, get_all_codelist_paths_for_schema
from validator.helpers.cogsresources import get_column_csv_paths_with_dfs_filtered_to_relevant, \
    get_column_underscored_names_for_obs_file, get_paths_and_dataframes_of_associated_csvs, \
    get_component_dfs_for_reference_repos_used, get_codelist_metadata_for_codelist_urls_in_schema
from validator.helpers.csv import get_csv_as_pandas
from validator.helpers.json import get_json_as_dict
from validator.helpers.pandas import assertions


def assert_cogs_implied_resources(validator, schema, **kwargs):
    """
    Confirm that the json an csv resources both listed and implied (components.csv etc) are
    reachable and can be read.

    :param validator: validator object
    :param schema: schema as dict
    :param kwargs:
    :return: None
    """

    implied_resources = get_cogs_implied_resources(schema, validator.local_ref)

    for resource in implied_resources:
        if resource.endswith(".csv"):
            get_csv_as_pandas(resource, "confirm implied csv resource is readable")
        elif resource.endswith(".json"):
            get_json_as_dict(resource, "confirm implied json resource is readable")
        else:
            validator.results.add_result("'{}' is not a valid resource type".format(resource),
                                         {"valid_types": ["csv", "json"]})

    # TODO we may be better off just calling csvlint here, investigate


def assert_field_mapping_between_tableschema_and_columns_csv(validator, schema, **kwargs):
    """
    This is one of out "do everything" checks. Basically we're confirming that where
    we slugize a to create a column name in the schema , i.e this:

        tableSchema: {
        columns: [
            {
            titles: "Geography",
            required: true,
            name: "geography",    <------ these ones
            datatype: "string"
            },
        {

    If matches the name field within one of the columns.csv files within a ref_* repo
    that is referenced from the schema.
    """

    column_paths_and_dfs = get_column_csv_paths_with_dfs_filtered_to_relevant(schema, validator.local_ref)
    column_names_found = get_column_underscored_names_for_obs_file(schema)

    all_column_csvs_checked = []
    for column in column_names_found:

        found = False
        for path, df in column_paths_and_dfs.items():
            all_column_csvs_checked.append(path)
            if column in df["name"].unique():
                found = True

        if not found:
            validator.results.add_result("column with name field '{}' does not exist in columns.csv's".format(column),
                            {"column_csvs_found_for_this_schema": all_column_csvs_checked})


def assert_components_csv_resources_are_correctly_mapped(validator, schema, **kwargs):
    """
    Get the relevent column df info, use this to determine which components entries we SHOULD have,
    compare with what we've got, report missing.
    """

    # Resources we will need
    column_dfs = get_column_csv_paths_with_dfs_filtered_to_relevant(schema, validator.local_ref)
    components_dfs = get_component_dfs_for_reference_repos_used(schema, validator.local_ref)

    component_types = [
        Box({"path": "http://gss-data.org.uk/def/dimension/", "qb":"qb:dimension", "title": "Dimension"}),
        Box({"path": "http://gss-data.org.uk/def/measure/", "qb": "qb:measure", "title": "Measure"}),
        Box({"path": "http://gss-data.org.uk/def/attribute/", "qb": "qb:attribute", "title": "Attribute"})
    ]

    for component in component_types:

        for path, df in column_dfs.items():

            # TODO - use names from schema, not hard coded
            # ------------
            # Dimensions
            dim_df = df[df["property_template"].map(lambda x: x.startswith(component.path)) == True]
            titles = list(dim_df["title"].unique())

            for title in titles:

                found = False
                component_type_given = None

                for comp_df in components_dfs:
                    if title in comp_df["Label"].unique():
                        found = True
                        component_type_given = list(comp_df["Component Type"][comp_df["Label"] == title].unique())[0]

                if component_type_given != component.title and component_type_given != None:
                    validator.results.add_result("The entry titled '{}' from column csv '{}' is type '{}' in "
                    "the columns file, but type '{}' in the components file".format(title, path, component.qb, component_type_given), {})

                if not found:
                    siginifying_entry = dim_df["property_template"][dim_df["title"] == title].unique()
                    validator.results.add_result("The entry titled '{}' from column csv '{}' requires an entry in components, "
                                               "but no component entry could be found".format(title, path),
                                                {"signifying property template entry": siginifying_entry})
                                                # TODO: it'd be nice to inlcude the path to components files


def assert_columns_csv_resources_are_correctly_formatted(validator, schema, **kwargs):
    """
    Hard to know where to draw the line with this. Will restrict it to those things that
    are burning us for now. We can always expand on this later.
    """


    # First formatting checks
    path_df_map = get_paths_and_dataframes_of_associated_csvs(schema, validator.local_ref, "columns.csv")

    for path, df in path_df_map.items():

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

        # TODO - check component attachment, i.e "http://gss-data.org.uk/def/dimension/" should be  "qb:dimension" etc


def assert_codelist_csv_resources_are_correctly_formatted(validator, schema, **kwargs):

    # TODO - refactor, not very good

    """
    Make sure the codelist csvs are correctly formatted
    """
    codelist_paths = get_all_codelist_paths_for_schema(schema, validator.local_ref)

    # Create a dict of {path to csv: pandas dataframe}
    path_and_df_dict = {}
    for path in codelist_paths:
        path_and_df_dict[path] = get_csv_as_pandas(path, "attemting to load '{}' for "
           "assert_codelist_csv_resources_are_correctly_formatted".format(path))

    # Compile re's here otherwise we're repeating ourselves
    notation_pattern = re.compile("[a-z0-9-]")

    for path, df in path_and_df_dict.items():

        # TODO - get all the columns headers from the json schema, so it wont break if/when we change our minds

        # -----------
        # Notation
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
                                                 {}) # TODO - it'd be nice to lists the non int's
                else:
                    # If we do, make sure there's an order to them
                    order = set(int_sort_fields)
                    for i in range(1, len(order)+1):
                        if i not in int_sort_fields:
                            validator.results.add_result("The sort priority field in '{}' is malformed."
                                                         " If we are using Sort Priority, the integers"
                                                         " should follow a sequence incrementing in 1's."
                                                         .format(path), {"sequence": order})
                            break