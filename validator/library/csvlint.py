
import os
import subprocess

def csvlint(validator, schema, **kwargs):
    """
    Basic structural linting based on the Open Data Institutes csvlint tool

    "param result: a results object, as defined in ../results.py
    :param schema: a dot notation dict of a csvw schema
    :return: results
    """

    # A catch so we can run in or out of the container
    try:
        whole_command = "csvlint -s" + validator.schema_path
        proc = subprocess.Popen(whole_command.split(" "), stdout=subprocess.PIPE)
    except FileNotFoundError:
        pwd = os.getcwd()
        whole_command = "docker run -v {}:/workspace -w /workspace gsscogs/csvlint csvlint -s ".format(pwd)  + validator.schema_path
        proc = subprocess.Popen(whole_command.split(" "), stdout=subprocess.PIPE)

    while True:
        line = proc.stdout.readline()
        if not line:
            break
        # the real code does filtering here
        if "INVALID" in  str(line):
            validator.results.add_result("one or more csvw files is INVALID, run "
                                        "the provided cmmand for more details", {"command": whole_command})
