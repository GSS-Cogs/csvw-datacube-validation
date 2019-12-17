
import pandas as pd

from library.helpers.observation_file import get_obs_file_table_schema

def confirm_schema_columns_name_match_obs_file_columns(validator, schema, **kwargs):

    obs_schema = get_obs_file_table_schema(schema)

    pd.read_csv(validator.obs_file_path)

    # TODO - do the things.

