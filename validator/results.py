
class Results(object):
    """
    A Results class to hold information from failed checks until such time as
    we're ready to output failures.
    """

    def __init__(self, name):
        self.name = name
        self.results = {}

    def add_result(self, id, check_name, details):

        if id not in self.results.keys():
            self.results.update({id:{}})

        if check_name in self.results[id]:
            raise Exception("Aborting. Attempting to add results for a check that we already have"
                            "a result for. Details: 'id:'{} , 'check_name:' {}, 'details:' {} "
                            .format(id, check_name, str(details)))

        self.results[id].update({check_name: details})

    def simple_print_results(self):
        """
        A Simple "print the results" method for development and debugging

        :return: None
        """
        print("")
        print("-------")
        print("Results")
        print("-------")
        print(self.name)
        print(self.results)
        print("")
