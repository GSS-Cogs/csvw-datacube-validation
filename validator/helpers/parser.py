
from box import BoxList, Box

from .exceptions import ConfigurationError

def get_keywords(things):
	for thing in things:
		if isinstance(thing, (list, BoxList)):
			for t in thing:
				return get_keywords(t)
		elif isinstance(thing, (dict, Box)):
			for k, v in thing.items():
				return {k, get_keywords(v)}
		else:
			return things

def make_instruction_from_step(st):

	if isinstance (st, str):
		ins = Box({st:{}})
	else:
		ins = get_keywords(st)

	# The very first parameter MUST
	# be a keyword argument.
	for _, v in ins.items():
		if isinstance(v, (list, BoxList)):
			raise ConfigurationError("Step arguments require at least one initial keyword, you cannot pass a list")
		break
	return ins
