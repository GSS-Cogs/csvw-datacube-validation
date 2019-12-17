

from library.helpers.reference import get_cogs_implied_resources

def assert_cogs_implied_resources(validator, schema, **kwargs):

    implied_resources = get_cogs_implied_resources(schema)

    print(implied_resources)

    # TODO - these things are reachable, csvs match schemas etc
    # note - is this one even necessary?
    # we may be better off just calling csvlint here.