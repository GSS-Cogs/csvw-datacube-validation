
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


