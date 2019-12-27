
import inspect

class Cacher(object):
    """
    The thing that stores the data for the cache decorator
    """

    def __init__(self):

        # TODO - if we don't need another, replace this class with a straight dict
        self.name_cache = {}


class cache(object):
    """
    cache allows you to mark some functions as having already been run against a given input.

    This  lets us safely run global checks like "check all columns data" without constantly repeating
    ourselves.
    """

    def __init__(self, f):
        self.f = f
        self.cache = shared_cache

    def __call__(self, *args, **kwargs):

        # Get the function name to cache
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        function_name = calframe[1][3]

        # Get the parameter to cahce
        first_parameter = args[1]

        if not isinstance(first_parameter, str):
            raise ValueError("Aborting, incorrect use of cache. The first argument must be a sting.")

        # if we've called this function with this argument before...no need to do it again
        do = True
        if function_name in self.cache.name_cache.keys():
            if first_parameter in self.cache.name_cache[function_name]:
                do = False
        else:
            self.cache.name_cache[function_name] = []

        if do:
            self.f(*args, **kwargs)
            self.cache.name_cache[function_name].append(first_parameter)
        else:
            return


shared_cache = Cacher()