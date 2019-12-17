
import os

from datacube import DataCubeValidator
from library.helpers.config import get_function_map_from_config
from library.helpers.yaml import load_controller_yaml
from library.helpers.exceptions import ConfigurationError


class Init:
    """
    Runs the tests for all datacubes as specified by the list of *-schema.json file(s) provided
    """

    def __init__(self, datacube_schemas, config_path=None, local_ref=False):
        self.datacube_schemas = datacube_schemas
        self.result_set = []

        # Load the config, this controls global settings as well as defining what checks to run and when
        if config_path == None:
            config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yaml")
        self.config = load_controller_yaml(config_path)

        # If local reference data has been allowed but no config has been given, bomb out now with a warning
        if local_ref and self.config.options.local_reference_substitution == None:
            raise ConfigurationError("To pass 'local_ref=True' you need to have some local"
                                     "references defined in your configuration yaml.")
        # TODO - the above is messy, there's a better way


        self.local_ref = local_ref

        # ----------------------
        # Build a map of the checking functions we're using
        self.func_map = get_function_map_from_config(self.config)

        # Run the tests
        self.do()

        # Get the results
        self.show_results()

    def do(self):

        for datacube in self.datacube_schemas:
            dcv = DataCubeValidator(datacube, self.config, self.func_map, self.local_ref)

            try:
                result = dcv.validate()
                self.result_set.append(result)
            except Exception as e:
                raise Exception("Error encountered while attempting to validate datacube '{}'."
                                .format(datacube)) from e

    def show_results(self):

        for result in self.result_set:
            # TODO - just blurting to screen for now, something snazzy would be better
            result.simple_print_results()


if __name__ == "__main__":

    # TODO - we're just hard coding one for now to develop against
    schemas = [
        "https://ci.floop.org.uk/job/GSS_data/job/Housing/job/WG-Chargeable-homes/lastSuccessfulBuild/artifact/out/observations.csv-schema.json"
    ]
    Init(schemas)
