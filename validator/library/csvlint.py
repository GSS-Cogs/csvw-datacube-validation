
import os
import subprocess

def csvlint(validator, schema, **kwargs):
    """
    Basic structural linting based on the Open Data Institutes csvlint tool

    "param result: a results object, as defined in ../results.py
    :param schema: a dot notation dict of a csvw schema
    :return: results
    """


    pwd = os.getcwd()
    try:
        base = "docker run -v {}:/workspace -w /workspace gsscogs/csvlint csvlint -s ".format(pwd)
    except:
        # We may be running inside a ruby container already
        base = "csvlint -s"

    whole_command = base + validator.schema_path

    # TODO - do we wrap csvlint or rerun it?
    proc = subprocess.Popen(whole_command.split(" "), stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        # the real code does filtering here
        if "INVALID" in  str(line):
            validator.results.add_result("one or more csvw files is INVALID, run "
                                        "the provided cmmand for more details", {"command": whole_command})
