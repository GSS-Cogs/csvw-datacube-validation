
import re

from box import Box

class begins_then_not_re(object):
    """
    Lets you create a function to pass to the pandas .apply() method that
    matches true if the text begins with "start_text" bit DOESNT match
    start_text+pattern.

    Note, you can do this with a conditional regex, but we're aiming for something
    a bit more readable than that.
    """
    def __init__(self, start_text, pattern):
        self.start_text = start_text
        self.pattern = re.compile(start_text+pattern)

    def __call__(self, val):

        # If it's not a str type, return False
        if not isinstance(val, str):
            return False

        # Ignore blanks
        if val == "" or val == "nan":
            return False

        # Otherwise, match where beings AND not match pattern
        if val.startswith(self.start_text):
            if self.pattern.match(val) == None:
                return True
            else:
                return False


# TODO - there's a way do to do this without the dict....can't remember
# For convenience we're putting all classes for .assert() into a dot notation dict
# i.e assertions.thing
assertions = Box({
    "begins_then_not_re": begins_then_not_re
})