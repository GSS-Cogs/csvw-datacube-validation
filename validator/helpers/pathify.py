
import re
from unidecode import unidecode

# NOTE - take directly from gss-utils (as it;s all we need from that library)
def pathify(label):
    """
      Convert a label into something that can be used in a URI path segment.
    """
    return re.sub(r'-$', '',
                  re.sub(r'-+', '-',
                         re.sub(r'[^\w/]', '-', unidecode(label).lower())))