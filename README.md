# csvw-datacube-validation

_note - initial stab, very much a work in progress._

A extensible framework for validating multi dimensional datasets as defined by a csvw schema.


### The gist

We start with a csvw file representing a dataset.

The validation that runs (the selection of functions to run, gathered in what groups, options etc) are defined within ./validator/config.yaml.

The choice of functions to run are defined within libraries, which as listed at the top of ./validator/config.yaml (there's a default /library I'm using for now). The idea being if you have a non standard use case - pass it some functions for it, and call them in your config.yaml.

The thought is that everything breaks down to tiny function all taking a signatues of (validatorObject, schema, kwargs), any functions that meets that signature can be included in the inventory and called by the validiator. Beyond that everything else is just wrapper.

So it _should_ be a highly extensible tool and easily adaptable to (a) other organisations and (b) changes in our own requirments.
