# csvw-datacube-validation

_note - initial stab, very much a work in progress._

A extensible framework for validating multi dimensional datasets as defined by a csvw schema.

### Install

Two options, I would personally use docker, but I've included both as the second is easier for development.

With docker:
- At the terminal `open ~/.bashrc` and add an alias `alias validate="docker run gsscogs/csvw-datacube-validation:latest /bin/bash /run.sh"`


To install locally:
-  `git clone https://github.com/GSS-Cogs/csvw-datacube-validation`
- cd in, then `pip3 install -r requirments.txt`


### Usage

The start point is **always** a csvw schema file represenenting a single dataset. So for COGS a json file ending `csv-schema.json`.

1.) Via Docker
- `validate <path-to-schema>`

2.) With a direct python install
- `python3 /path-to-the-repo/init.py <path-to-schema>`  
  
Path to schema can always be a url, eg "https://ci.floop.org.uk/job/GSS_data/job/Disability/job/PHE-Co-occurring-substance-misuse-and-mental-health-issues/82/artifact/datasets/PHE-Co-occurring-substance-misuse-and-mental-health-issues/out/county-ua-deprivation-deciles-in-england-imd2010.csv-schema.json", but to validate using local reference sources you need a little more setup (see below).


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
