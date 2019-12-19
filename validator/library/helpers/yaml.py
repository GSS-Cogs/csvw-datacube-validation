
import yaml

from box import Box
from .exceptions import ConfigurationError

def load_yaml(path_to_yaml):

    with open(path_to_yaml, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # put in Box for dot notation
    config = Box(data)

    return config


def confirm_valid_config(path_to_yaml):
    """
    Make sure config is valid. Try and provide meaningful exceptions where the
    user has got it wrong.

    :param config: config dict
    :return: config
    """

    config = load_yaml(path_to_yaml)

    required_root_keys = ["stages", "options"]
    for rrk in required_root_keys:
        if rrk not in config.keys():
            raise ConfigurationError("Your configuration must include a '{}' key."
                                     .format(rrk))

    execution_order_list = []
    for stage_name in config.stages:
        if config.stages[stage_name].execution_order in execution_order_list:
            raise ConfigurationError("You cannot have two stages with the same "
                                     "execution order.")

    return config
