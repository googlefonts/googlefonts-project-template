import sys

from pip_api._vendor.packaging import version as packaging_version

# Import this now because we need it below
from pip_api._version import version

PIP_VERSION = packaging_version.parse(version())
PYTHON_VERSION = sys.version_info

# Import these because they depend on the above
from pip_api._hash import hash
from pip_api._installed_distributions import installed_distributions

# Import these whenever, doesn't matter
from pip_api._parse_requirements import parse_requirements
