
from box import Box, BoxList
import datetime

from colorama import Fore, Style
from texttable import Texttable

from results import Results
from constants import LINE_BREAK
from library.helpers.json import get_json_as_dict
from library.helpers.exceptions import ConfigurationError
from library.helpers.observation_file import get_obs_path_from_schema

class DataCubeValidator():
    """Controls validation for a single datacube as defined by a single *-schema.json file."""

    def __init__(self, path_or_url, config, function_map, local_ref):
        self.local_ref = local_ref
        self.config = config
        self.results = Results(path_or_url)
        self.schema_path = path_or_url
        self.schema = get_json_as_dict(path_or_url, "loading initial schema for datacube")
        self.function_map = function_map
        self.obs_file_path = get_obs_path_from_schema(self.schema, path_or_url)

    def validate(self):

        print(Fore.GREEN + LINE_BREAK)
        print("for: ", self.schema_path)
        print("--- doing ---", Style.RESET_ALL)


        # Run through the stages as defined by the execution order
        # TODO - better, this is kinda nasty
        execution_order = set([v["execution_order"] for k,v in self.config.stages.items()])
        for eo in execution_order:
            stage_dict = [v for k,v in self.config.stages.items() if v["execution_order"] == eo][0]

            for step in stage_dict.steps:

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

            # TODO printing based on results. This should be pulled out
            if name not in self.results.results.keys():
                print(Fore.GREEN+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), stage_dict.description)
            else:
                print(Fore.RED+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), stage_dict.description)

                # TODO - this should be its own function
                # also, we might not want to print like this, or print at all
                for problem, details in self.results.results[name].items():

                    # Use a fancy text table for readibility
                    table = [["problem ==> ", problem]]
                    for k, v in details.items():
                        table.append([k, v])

                    t = Texttable()
                    t.add_rows(table)
                    print(t.draw())
                    print("")

                # If stop on fail, stop looping through stages for this schema
                if stage_dict.stop_on_fail:
                    break

        # Reset fancy green font
        print(Style.RESET_ALL)

        return self.results
