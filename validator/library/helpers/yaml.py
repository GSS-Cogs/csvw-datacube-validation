
import yaml

from box import Box

def load_controller_yaml(path):

    with open(path, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return Box(data)