
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


def get_paths_and_dataframes_of_associated_csvs(schema, local_ref, file_name):
    """
    Get dataframes  for all columns.csv files relevent to a give file we're trying to
    load. Filter to just the fields that matter to the task in hand, then return

    :param schema:  schema as dict
    :return:  dict of  {path to: pandas dataframes)
    """

    paths_to_columns_csvs = [x for x in get_cogs_implied_resources(schema, local_ref) if x.endswith(file_name)]

    path_df_map = {}
    for csv_path in paths_to_columns_csvs:
        df = get_csv_as_pandas(csv_path, "load columns csv as part of 'assert_columns_csv_resources_are_correct' function")
        path_df_map[csv_path] = df

    return path_df_map



def get_component_csv_paths_with_dfs_for_reference_repos_used(schema, local_ref):
    """
    Get a list of components csvs referenced by this dataset, as dataframes

    :param schema: csvw schema
    :param local_ref: local reference override dict
    :return: list of pandas dataframes
    """

    msg = "getting components.csv as part of 'get_component_dfs_for_reference_repos_used', using path '{}'"

    component_paths = [x for x in get_cogs_implied_resources(schema, local_ref) if x.endswith("components.csv")]

    path_df_dict = {}
    for path in component_paths:
        path_df_dict[path] = get_csv_as_pandas(path, msg.format(path))

    return path_df_dict


def get_column_csv_paths_with_dfs_filtered_to_relevant(schema, local_ref):
    """
    Wrapper, for when we only want the column dataframes from:
    get_paths_and_dataframes_of_associated_csvs
    """

    path_df_map = get_paths_and_dataframes_of_associated_csvs(schema, local_ref, "columns.csv")
    fields_required = get_column_underscored_names_for_obs_file(schema)
    filtered_list_of_dfs = {}

    for path, df in path_df_map.items():
        df = df[df["name"].map(lambda x: x in fields_required)]
        filtered_list_of_dfs[path] = df

    return filtered_list_of_dfs
