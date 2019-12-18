
from pprint import pprint
from colorama import Fore, Style

from constants import LINE_BREAK

class Results(object):
    """
    A Results class to hold information from failed checks until such time as
    we're ready to output failures.
    """

    def __init__(self, name):
        self.name = name
        self.results = {}
        self.checking = None

    def add_result(self, check_name, details):

        if self.checking not in self.results.keys():
            self.results.update({self.checking: {}})

        if check_name in self.results[self.checking].keys():
            raise Exception("Aborting. Attempting to add results for a check that we already have"
                            "a result for. Details: 'id:'{} , 'check_name:' {}, 'details:' {} "
                            .format(self.checking, check_name, str(details)))

        self.results[self.checking].update({check_name: details})

    def simple_print_results(self):
        """
        A Simple "print the results" method for development and debugging

        :return: None
        """
        # TODO - a real one
        if self.results != {}:
            print(Fore.RED + LINE_BREAK)
            print("Schema", self.name)
            pprint(self.results)
            print(LINE_BREAK, Style.RESET_ALL)

