# csvw-datacube-validation

_note - initial stab, very much a work in progress._

A extensible framework for validating multi dimensional datasets as defined by a csvw schema.

### What it does

You use a config file (see https://github.com/GSS-Cogs/csvw-datacube-validation/blob/master/validator/config.yaml) to define what you're validating in terms of stages made up of "steps".

Each "step" is a functions, as defined here https://github.com/GSS-Cogs/csvw-datacube-validation/tree/master/validator/library

The app takes care of the task running, reporting etc and provides accesss the various reference and data resources as defined by the csvw schema file.


### Install

To install locally:
-  `git clone https://github.com/GSS-Cogs/csvw-datacube-validation`
- cd in, then `pip install -r requirements.txt`


### Usage

The start point is **always** a csvw schema file represenenting a single dataset. So for COGS a json file ending `csv-schema.json`.

For now we need to run the python script directly
`python3 <wherever-you-cloned-it>/csvw-datacube-validation/run.py <path-to-schema>`

For convenience it's probably worth creating an alias by adding `alias validate="python3 <PATH TO WHERE YOU CLONES IT>/csvw-datacube-validation/run.py` to your `./bashrc` so you can use via `validate <path-to-schema>`.
  
Path to schema can always be a url, eg "https://ci.floop.org.uk/job/GSS_data/job/Disability/job/PHE-Co-occurring-substance-misuse-and-mental-health-issues/82/artifact/datasets/PHE-Co-occurring-substance-misuse-and-mental-health-issues/out/county-ua-deprivation-deciles-in-england-imd2010.csv-schema.json", and you can use locally held scheama files - but - if you want to validate against your locally held reference data (eg `/ref_common` or `/family-disabily/reference/`) you'll need to set up local reference sources (see below).


### Setup Local References

Validating things after they're gotten online is always going to be limited. You can choose to check your local version
of reference material (i.e columns.csv, components.csv) instead (there's a flag) but first we need to let the app know where those files are.

A few stages to set this up.

1.) Find somewhere convenient and create a yaml file (I use `substitutes.yaml` but the name doesnt matter).

2.) Map your references in it as per the below example:

```
/family-disability/: /Users/adamsm/go/src/github.com/GSS-Cogs/family-disability/
/ref_common/: /Users/adamsm/go/src/github.com/GSS-Cogs/ref_common/
```
*explanation - that's telling the app that when I want to use locally held reference data and
`/family-disability/` is in the path, go to `/Users/adamsm/go/src/github.com/GSS-Cogs/family-disability/` instead.*

To run in local reference mode include the `-r` flag when you run the app and point to where you saved your yaml file, i.e `validate -r /path-to/substitutes.yaml <path-to-schema>`.
