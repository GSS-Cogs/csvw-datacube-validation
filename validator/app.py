
import os

from .datasetvalidator import DatasetValidator
from .helpers.config import get_function_map_from_config
from .helpers.yaml import confirm_valid_config, load_yaml
from .helpers.exceptions import ConfigurationError

class Initialise:
    """
    Runs the tests for all datacubes as specified by the list of *-schema.json file(s) provided
    """

    def __init__(self, datacube_schemas, local_ref_path, config_path=None):

        self.datacube_schemas = datacube_schemas
        self.result_set = []

        # Load the config, this controls global settings as well as defining what checks to run and when
        if config_path == None:
            config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yaml")
        self.config = confirm_valid_config(config_path)

        # Get our local reference directories from
        if local_ref_path != None:
            try:
                self.local_ref = load_yaml(local_ref_path)
            except Exception as e:
                raise ConfigurationError("Unable to load a yaml file from the provided path '{}'."
                                         .format(local_ref_path)) from e
        else:
            self.local_ref = {}

        # ----------------------
        # Build a map of the checking functions we're using
        self.func_map = get_function_map_from_config(self.config)


    def create_jobs(self):
        """
        Create one job as object of type DataCubeValidator for each schema we've been provided
        """
        self.jobs = []
        for datacube in self.datacube_schemas:
            self.jobs.append(DatasetValidator(datacube, self.config, self.func_map, self.local_ref))


    def run_jobs(self):
        """
        Run .validate for each DataCubeValidator objects stored in the self.jobs list
        """
        for job in self.jobs:

            try:
                result = job.validate()

                # These should probably be separate things
                self.result_set.append(result)

            except Exception as e:
                raise Exception("Error encountered while attempting to validate datacube '{}'."
                                .format(job)) from e
