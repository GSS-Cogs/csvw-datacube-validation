
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


    def do(self):

        for datacube in self.datacube_schemas:
            dcv = DataCubeValidator(datacube, self.config, self.func_map, self.local_ref)

            try:
                result = dcv.validate()

                # These should probably be seperate things
                self.result_set.append(result)

            except Exception as e:
                raise Exception("Error encountered while attempting to validate datacube '{}'."
                                .format(datacube)) from e



if __name__ == "__main__":

    # TODO - we're just hard coding some for now to develop against
    schemas = [
        "https://ci.floop.org.uk/job/GSS_data/job/Housing/job/WG-Chargeable-homes/lastSuccessfulBuild/artifact/out/observations.csv-schema.json",
        "https://ci.floop.org.uk/job/GSS_data/job/Disability/job/NHS-guardianship-mental-health-act/27/artifact/datasets/NHS-guardianship-mental-health-act/out/cases-of-guardianship-under-the-mental-health-act-1983-by-gender-section-and-relationship-of-guardian.csv-schema.json",
        "https://ci.floop.org.uk/job/GSS_data/job/Disability/job/PHE-Co-occurring-substance-misuse-and-mental-health-issues/lastSuccessfulBuild/artifact/datasets/PHE-Co-occurring-substance-misuse-and-mental-health-issues/out/county-ua-deprivation-deciles-in-england-imd2015-419-geog.csv-schema.json",
        "https://ci.floop.org.uk/job/GSS_data/job/Disability/job/DfE-special-educational-needs/lastSuccessfulBuild/artifact/datasets/DfE-special-educational-needs/out/observations.csv-schema.json"
    ]
    Init(schemas)
