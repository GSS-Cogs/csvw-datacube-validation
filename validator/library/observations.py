
"""
from validator.helpers.reference import get_all_codelist_paths_for_schema
from validator.helpers.observation_file import get_obs_tableschema_from_schema
from validator.helpers.csv import get_csv_as_pandas
from validator.cacher import cache


def compare_observation_file_dimensions_with_codelists(validator, schema, **kwargs):

    # The one's we have specified directly
    codelist_paths = get_all_codelist_paths_for_schema(schema, validator.local_ref)

    df = get_csv_as_pandas(validator.obs_file_path, "Loading observation file for validating of codelist content")

    foreign_keys = get_obs_tableschema_from_schema(schema).foreign_keys

    for path in codelist_paths:
        validate_observations_csv_against_codelists(validator, path, df, foreign_keys)

@cache
def validate_observations_csv_against_codelists(validator, codelist_path, df, foreign_keys):

    # Get the designated column header, using the obs_table_schema
    for each in foreign_keys():
        print(each)

"""

