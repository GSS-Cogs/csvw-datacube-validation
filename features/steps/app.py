
import os

from behave import given, then
import pandas as pd

from validator.app import Initialise

@given('I initialise the app with an argument of schema "{schema}"')
def step_impl(context, schema):
    abs_path = os.path.dirname(os.path.realpath(__file__)) + schema
    context.app = Initialise([abs_path], None)

@given(u'specify a local reference file of "{yaml_path}"')
def step_impl(context, yaml_path):
    abs_path = os.path.dirname(os.path.realpath(__file__)) + yaml_path
    context.app = Initialise(context.app.datacube_schemas, abs_path)

@given('I create a validation task from that schema')
def step_impl(context):
    context.app.create_jobs()

@then('the config contains the keys: "{keys}"')
def step_impl(context, keys):
    keys_as_list = keys.split(",")
    for key in keys_as_list:
        assert key in context.app.config

@then('the function map contains the function "{func}"')
def step_imp(context, func):
    assert func in context.app.func_map

@then('I have local references for: "{local_refs}"')
def step_impl(context, local_refs):
    print(context.app.local_ref.keys())
    for ref in local_refs.split(","):
        assert ref in context.app.local_ref.keys()

@then('the derrived observation file path ends with "{path_ends_with}"')
def step_impl(context, path_ends_with):
    assert context.app.jobs[0].obs_file_path.endswith(path_ends_with)

@then('the observation csv for job "{job_no}" can be loaded into pandas')
def step_impl(context, job_no):
    pd.read_csv(context.app.jobs[int(job_no)].obs_file_path)