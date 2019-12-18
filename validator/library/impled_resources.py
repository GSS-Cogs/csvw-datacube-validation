
import re

from library.helpers.reference import get_cogs_implied_resources
from library.helpers.cogs_specific_csvs import get_column_dataframes_relevent_to_an_observation_file, get_column_underscored_names_for_obs_file
from library.helpers.csv import get_csv_as_pandas
from library.helpers.json import get_json_as_dict

def assert_cogs_implied_resources(validator, schema, **kwargs):

    implied_resources = get_cogs_implied_resources(schema)

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
    columns_paths = [x for x in get_cogs_implied_resources(schema) if x.endswith("columns.csv")]
    column_dfs = get_column_dataframes_relevent_to_an_observation_file(schema)
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


    column_dfs = get_column_dataframes_relevent_to_an_observation_file(schema)

    snake_pattern = re.compile("")
    kebad_pattern = re.compile("")

    for df in column_dfs:

        for i, row in df.iterrows():


            if str(row["property_template"]).startswith(our_dim_prefix):

                # Last values in property_template url
                value_should_be_kebbabed = entry(row, "property_template", -1)
                if not kebad_pattern.match(value_should_be_kebbabed):
                    validator.results.add_result(
                        "value '{}' is incorrect for property_template".format(value_should_be_kebbabed),
                        {"expected (example)": "http://gss-data.org.uk/def/dimension/residential-status"})

            if str(row["value_template"]).startswith(our_concept_prefix):

                # Second to last value in value_template url
                value_should_be_kebbabed = entry(row, "value_template", -2)
                if not kebad_pattern.match(value_should_be_kebbabed):
                    validator.results.add_result(
                        "value '{}' is incorrect for value_template".format(value_should_be_kebbabed),
                        {"expected (example)": "http://gss-data.org.uk/def/concept/residential-status/{residential_status}"})

                # Last value in value_template url
                value_should_be_kebbabed = entry(row, "value_template", -1)[1:-1]
                if not snake_pattern.match(value_should_be_kebbabed):
                    validator.results.add_result(
                        "value '{}' is incorrect for value_template".format(value_should_be_kebbabed),
                        {"expected (example)": "http://gss-data.org.uk/def/concept/residential-status/{residential_status}"})










