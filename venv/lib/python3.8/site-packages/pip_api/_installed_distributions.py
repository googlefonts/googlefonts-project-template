import re

import pip_api
from pip_api._call import call

from pip_api._vendor.packaging.version import parse


class Distribution:
    def __init__(self, name, version, location=None):
        self.name = name
        self.version = parse(version)
        self.location = location
        self.editable = bool(self.location)

    def __repr__(self):
        return "<Distribution(name='{}', version='{}'{})>".format(
            self.name,
            self.version,
            ", location='{}'".format(self.location) if self.location else "",
        )


def _old_installed_distributions():
    result = call("list")

    # result is of the form:
    # <package_name> (<version>)
    #
    # or, if editable
    # <package_name> (<version>, <location>)
    #
    # or, could be a warning line

    ret = {}

    pattern = re.compile(r"(.*) \((.*)\)")

    for line in result.strip().split("\n"):
        match = re.match(pattern, line)

        if match:
            name, paren = match.groups()
            version, location = (paren.split(", ") + [None])[:2]

            ret[name] = Distribution(name, version, location)
        else:
            # This is a warning line or some other output
            pass

    return ret


def _new_installed_distributions():
    result = call("list", "--format=columns")

    # result is of the form:
    # <package_name>   <version>
    #
    # or, if editable
    # <package_name>   <version>   <location>
    # (with arbitrary spaces)

    ret = {}

    # Remove first two heder lines
    lines = result.strip().split("\n")[2:]

    for line in lines:
        # Split on whitespace to get
        # split = ['<name>', '<version>', '<location>'|None]
        split = line.split() + [None]
        name = split[0]
        version = split[1]
        location = split[2]

        ret[name] = Distribution(name, version, location)

    return ret


def installed_distributions():
    if pip_api.PIP_VERSION < parse("9.0.0"):
        return _old_installed_distributions()
    return _new_installed_distributions()
