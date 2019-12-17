
def csvlint(validator, schema, **kwargs):
    """
    Basic structural linting based on the Open Data Institutes csvlint tool

    "param result: a results object, as defined in ../results.py
    :param schema: a dot notation dict of a csvw schema
    :return: results
    """

    # TODO - do we wrap csvlint or rerun it?
