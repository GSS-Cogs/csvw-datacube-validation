
from .reference import get_cogs_implied_resources
from .observation_file import get_obs_file_table_schema
from .csv import get_csv_as_pandas

def get_column_underscored_names_for_obs_file(schema):
    """
    Get all the slugged names of column for an observation file

    i.e this:

    tableSchema: {
        columns: [
            {
            titles: "Geography",
            required: true,
            name: "geography",    <------ these ones
            datatype: "string"
            },
        {

    :return: list
    """
    obs_table = get_obs_file_table_schema(schema)
    return [x["name"] for x in obs_table["tableSchema"]["columns"]]


def get_column_dataframes_relevent_to_an_observation_file(schema, local_ref):
    """
    Get dataframes  for all columns.csv files relevent to a give file we're trying to
    load. Filter to just the fields that matter to the task in hand, then return

    :param schema:  schema as dict
    :return:  list of pandas dataframes
    """

    fields_required = get_column_underscored_names_for_obs_file(schema)

    paths_to_columns_csvs = [x for x in get_cogs_implied_resources(schema, local_ref) if x.endswith("columns.csv")]

    initial_data_frames = []
    for csv_path in paths_to_columns_csvs:
        initial_data_frames.append(
            get_csv_as_pandas(csv_path, "load columns csv as part of 'assert_columns_csv_resources_are_correct' function")
        )

    data_frames = []
    for df in initial_data_frames:
        df = df[df["name"].map(lambda x: x in fields_required)]
        data_frames.append(df)

    # Make sure we have one columns.csv file entry for every concept
    all_entries = 0
    for df in data_frames:
        all_entries += len(df)

    return data_frames

