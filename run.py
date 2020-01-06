
import argparse

from validator.app import Initialise

if __name__ == "__main__":
    # TODO - flag for display fails as found

    parser = argparse.ArgumentParser()
    parser.add_argument("path_or_url", help="a single path or url")
    parser.add_argument("-l", action='store_true')
    args = parser.parse_args()

    # TODO - for now we're just listifying a single path/url
    # what we want is to .walk() where it's a directory path and pass through a list

    validation = Initialise([args.path_or_url], args.l, display_fails_as_found=True)
    validation.create_jobs()
    validation.run_jobs()

    # TODO at this point we have all the results stored in self.result_set....do we want to anything with them?
