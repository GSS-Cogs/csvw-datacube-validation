
import os
import importlib.util

from inspect import getmembers, isfunction

from .exceptions import ConfigurationError


def get_function_map_from_config(config):
    """
    Check that there are no clashes between the default checks and any checks passed in via
    the config.

    Check that all checks requested via the config exist and have provided arguments that match
    their signature.

    Make sure that we have a valid execution order for the functions supplied.

    Create a map of "function name": function for later

    :param config:  config dict
    :return: {func name:  function}
    """

    # Required for relative paths / from main script directroy (i.e library)
    this_dir = os.path.dirname(os.path.realpath(__file__))
    path_to_home = "/".join(this_dir.split("/")[:-2])

    # Import all the modules
    function_map = {}
    for source in config.options.module_sources:

        if source == "/library":
            source = path_to_home + source
            function_map = update_map_from_local_dir(function_map, source)
        else:
            raise NotImplementedError("The ability to use other package sources has"
                                      "not been implemented yet.")

    return function_map


def update_map_from_local_dir(function_map, source_dir):

    all_files = [x for x in os.listdir(source_dir) if x.endswith(".py")]

    for path in all_files:
        function_map = update_map_from_file(function_map, source_dir + "/" + path)

    return function_map


def update_map_from_file(function_map, path):

    # Import the provided .py as a module
    spec = importlib.util.spec_from_file_location("module.name", path)
    temp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(temp_module)

    # Use inspect to pull out the functions and map them to the names
    function_tuples = [o for o in getmembers(temp_module) if isfunction(o[1])]
    for function_tuple in function_tuples:

        if function_tuples[0] in function_map.keys():
            raise ConfigurationError("You have more than one function mapped to the same name")

        function_map[function_tuple[0]] = function_tuple[1]

    return function_map