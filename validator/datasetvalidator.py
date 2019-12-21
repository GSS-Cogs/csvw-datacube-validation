
import datetime

from box import Box, BoxList
from colorama import Fore, Style
from texttable import Texttable

from .results import Results
from .helpers.json import get_json_as_dict
from .helpers.exceptions import ConfigurationError
from .helpers.observation_file import get_obs_path_from_schema
from .helpers.parser import make_instruction_from_step

LINE_BREAK = "-----------------------------------"

class DatasetValidator():
    """Controls validation for a single datacube as defined by a single *-schema.json file."""

    def __init__(self, path_or_url, config, function_map, local_ref, display_fails_as_found):
        self.local_ref = local_ref
        self.config = config
        self.display_as_found = display_fails_as_found
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

            displayed_stage_name = False
            for step in stage_dict.steps:

                instruction = make_instruction_from_step(step)
                for function_name, step_kwargs in instruction.items():

                    self.results.checking = function_name
                    self.function_map[function_name](self, self.schema, **step_kwargs)
                    self.results.checking = None

                # TODO printing based on results. This should be pulled out
                if not displayed_stage_name:
                    print("\n" + Fore.BLUE + stage_dict.description)
                    displayed_stage_name = True

                if function_name not in self.results.results.keys():
                    print(Fore.GREEN+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), function_name)
                else:
                    print(Fore.RED+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), function_name)

                    # TODO - this should be its own function
                    # also, we might not want to print like this, or print at all
                    for problem, details in self.results.results[function_name].items():

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
