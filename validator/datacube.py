
from box import Box, BoxList
import datetime

from colorama import Fore, Style

from results import Results
from constants import LINE_BREAK
from library.helpers.json import get_json_as_dict
from library.helpers.exceptions import ConfigurationError
from library.helpers.observation_file import get_obs_path_from_schema

class DataCubeValidator():
    """Controls validation for a single datacube as defined by a single *-schema.json file."""

    def __init__(self, path_or_url, config, function_map, local_ref):
        self.config = config
        self.local_ref = local_ref
        self.results = Results(path_or_url)
        self.schema_path = path_or_url
        self.schema = get_json_as_dict(path_or_url, "loading initial schema for datacube")
        self.function_map = function_map
        self.obs_file_path = get_obs_path_from_schema(self.schema, path_or_url)

    def validate(self):

        print(Fore.GREEN + LINE_BREAK)
        print("for: ", self.schema_path)
        print("--- doing ---", Style.RESET_ALL)

        # What checks we run and under what heading is defined by the config
        for group_name, function_dict in self.config.checking_rounds.items():

            for step in function_dict.steps:


                # TODO - if the result object has populated and stop_on_fail == True
                # we need to skip further rounds of validation


                # If the step has keyword arguments, get them

                # TODO - this is awful!!!
                # TODO - do a resursive thingy to get all the kwargs

                step_kwargs = {}
                if type(step) == str:
                    name = step
                elif type(step) == dict or type(step) == Box:
                    for k, v in step.items():
                        name = k
                        if isinstance(v, dict) or isinstance(v, Box):
                            for k2, v2 in v.items():
                                step_kwargs[k2] = v2
                        else:
                            if isinstance(v, list) or isinstance(v, BoxList):
                                for sub_step in v:
                                    if isinstance(sub_step, dict) or isinstance(sub_step, Box):
                                        for k3, v3 in sub_step.items():
                                            step_kwargs[k3] = v3
                                    else:
                                        # ewww
                                        raise ConfigurationError("Configuration not accounted for: " + str(sub_step))
                            else:
                                step_kwargs[k] = v
                else:
                    raise ConfigurationError("Config steps can only be dictionary items or strings"
                                             ", the step '{}' is a '{}'.".format(step, str(type(step))))

                self.results.checking = name
                self.function_map[name](self, self.schema, **step_kwargs)
                self.results.checking = None

            if name not in self.results.results.keys():
                print(Fore.GREEN+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), function_dict.description)
            else:
                print(Fore.RED+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), function_dict.description)
                print(self.results.results[name])

        # Reset fancy green font
        print(Style.RESET_ALL)

        return self.results
