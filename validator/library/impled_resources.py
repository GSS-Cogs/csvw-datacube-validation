
import re

from library.helpers.reference import get_cogs_implied_resources
from library.helpers.cogs_specific_csvs import get_column_dataframes_relevent_to_an_observation_file, get_column_underscored_names_for_obs_file
from library.helpers.csv import get_csv_as_pandas
from library.helpers.json import get_json_as_dict

def assert_cogs_implied_resources(validator, schema, **kwargs):

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


def assert_all_required_columns_csv_fields_exist(validator, schema, **kwargs):
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

    # TODO - three seperate calls can't be right
    columns_paths = [x for x in get_cogs_implied_resources(schema, validator.local_ref) if x.endswith("columns.csv")]
    column_dfs = get_column_dataframes_relevent_to_an_observation_file(schema, validator.local_ref)
    column_names_found = get_column_underscored_names_for_obs_file(schema)

    for column in column_names_found:

        found = False
        for df in column_dfs:
            if column in df["name"].unique():
                found = True

        if not found:
            validator.results.add_result("column with name field '{}' does not exist in columns.csv's".format(column),
                            {"column_csvs_found_for_this_schema": columns_paths})



def assert_columns_csv_resources_are_correct(validator, schema, **kwargs):
    """
    Hard to know where to draw the line with this. Will restrict it to those things that
    are burning us for now. We can always expand on this later.
    """

    # Save some space
    our_dim_prefix = "http://gss-data.org.uk/def/dimension/"
    our_concept_prefix = "http://gss-data.org.uk/def/concept/"

    def entry(row, column, index):
        return row[column].split("/")[index]


    column_dfs = get_column_dataframes_relevent_to_an_observation_file(schema, validator.local_ref)

    snake_pattern = re.compile("^[a-z0-9_]*$")
    kebab_pattern = re.compile("^[a-z0-9-]*$")

    for df in column_dfs:

        for i, row in df.iterrows():

            if str(row["property_template"]).startswith(our_dim_prefix):

                # Last values in property_template url
                val = entry(row, "property_template", -1)
                match = kebab_pattern.match(val)
                if not match:
                    validator.results.add_result(
                        "The value '{}' is incorrect for column 'property_template'".format(val),
                        {"expected (example)": "http://gss-data.org.uk/def/dimension/styled-like-this",
                         "got": row["property_template"], "problem_field": val})

            if str(row["value_template"]).startswith(our_concept_prefix):

                # Second to last value in value_template url
                val = entry(row, "value_template", -2)
                match = kebab_pattern.match(val)
                if not match:
                    validator.results.add_result(
                        "The value '{}' is incorrect for column 'value_template'".format(val),
                        {"expected (example)": "http://gss-data.org.uk/def/concept/styled-like-this/{styled_like_this}",
                         "got": row["value_template"], "problem_field": val})

                # Last value in value_template url
                val = entry(row, "value_template", -1)
                match = snake_pattern.match(val[1:-1])
                if not match:
                    validator.results.add_result(
                        "The value '{}' is incorrect for column 'value_template'".format(val),
                        {"expected (example)": "http://gss-data.org.uk/def/concept/styled-like-this/{styled_like_this}",
                         "got": row["value_template"], "problem_field": val})
