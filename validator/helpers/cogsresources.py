
from .reference import get_cogs_implied_resources, get_all_codelist_paths_for_schema
from .observation_file import get_obs_file_table_schema
from .generic import all_dict_values, is_url, localise
from .csv import get_csv_as_pandas
from .json import get_json_as_dict


def get_schemas_for_reference_repos(schema, schema_name):
    """
    Find the metadata schemas for all reference repos relevant to a
    given csvw.

    :param schema: schema as dict
    :name: the name of the schemas we're looking for, i.e 'codelists-metadata.json'
    :return: list of urls
    """

    links = [x for x in all_dict_values(schema) if is_url(x) and x.endswith(schema_name)]
    return [localise(x, schema.local_ref) for x in links]


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


def get_codelist_metadata_dicts(schema, local_ref):
    """
    Get the codelist-metadata json links

    :return: [ url fo codelist-metadata-jsons ]
    """

    json_paths = [x for x in get_cogs_implied_resources(schema, local_ref) if x.endswith("codelists-metadata.json")]
    return [get_json_as_dict(x, "getting codelist-json from '{}' as dict".format(x)) for x in json_paths]


def get_codelist_metadata_for_codelist_urls_in_schema(schema, local_ref):
    """
    Get a list of metadata for any codelists directly referenced in the schema

    i.e list of this kinda thing
    {
    "url": "codelists/employment-status.csv",
    "tableSchema": "https://gss-cogs.github.io/ref_common/codelist-schema.json",
    "rdfs:label": "Employment Status"
    }
    """

    codelists_for_schema = get_all_codelist_paths_for_schema(schema, local_ref)
    codelist_metadata_jsons_for_schema = [get_json_as_dict(x, "TODO") for x in get_cogs_implied_resources(schema, local_ref) if
                                    x.endswith("codelists-metadata.json")]

    # Create a mapping of the relative path of codelists to absolute path
    codelist_path_mapping = {"/".join(x.split("/")[-2:]):x for x in codelists_for_schema}

    relevant_codelist_metadata = []
    for codelist_metadata_json in codelist_metadata_jsons_for_schema:
        for metadata_entry in codelist_metadata_json["tables"]:
            if metadata_entry["url"] in codelist_path_mapping.keys():
                relevant_codelist_metadata.append(metadata_entry)

    return relevant_codelist_metadata


def get_component_dfs_for_reference_repos_used(schema, local_ref):
    """
    Get a list of components csvs referenced by this dataset, as dataframes

    :param schema: csvw schema
    :param local_ref: local reference override dict
    :return: list of pandas dataframes
    """

    msg = "getting components.csv as part of 'get_component_dfs_for_reference_repos_used', using path '{}'"

    component_csvs = [get_csv_as_pandas(x, msg.format(x)) for x in get_cogs_implied_resources(schema, local_ref)
                      if x.endswith("components.csv")]

    return component_csvs


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
