
import os
import sys
import argparse

from datacube import DataCubeValidator
from library.helpers.config import get_function_map_from_config
from library.helpers.yaml import confirm_valid_config, load_yaml
from library.helpers.exceptions import ConfigurationError

class Init:
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

        # Run the tests
        self.do()


    def do(self):

        for datacube in self.datacube_schemas:
            dcv = DataCubeValidator(datacube, self.config, self.func_map, self.local_ref)

            try:
                result = dcv.validate()

                # These should probably be separate things
                self.result_set.append(result)

            except Exception as e:
                raise Exception("Error encountered while attempting to validate datacube '{}'."
                                .format(datacube)) from e



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("path_or_url", help="a single path or url")
    parser.add_argument("-r", "--reference", nargs='?', default=None)
    args = parser.parse_args()

    # TODO - for now we're just listifying a single path/url
    # what we want is to .walk() where it's a directory path and pass through a list

    Init([args.path_or_url], args.reference)

