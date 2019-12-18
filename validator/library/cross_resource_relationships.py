
import pandas as pd

from library.helpers.reference import get_cogs_implied_resources
from library.helpers.observation_file import get_obs_file_table_schema
from library.helpers.exceptions import BadReferalError
from library.helpers.csv import get_csv_as_pandas


def confirm_obs_file_columns_appear_in_meatadata_schema(validator, schema, **kwargs):

    obs_schema = get_obs_file_table_schema(schema)

    pd.read_csv(validator.obs_file_path)

    # TODO - do the things.

