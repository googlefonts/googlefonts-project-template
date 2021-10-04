#!/usr/bin/env python3

# This script is run the first time any action is performed after the repository
# is cloned. If you are reading this because the automatic initialization failed,
# skip down to the section headed "INITIALIZATION STEPS".

from sh import git
import re
import sys
from urllib.parse import quote

BASE_OWNER = "googlefonts"
BASE_REPONAME = "Unified-Font-Repository"


def repo_url(owner, name):
    return f"https://github.com/{owner}/{name}"


def web_url(owner, name):
    return f"https://{owner}.github.io/{name}"


def raw_url(owner, name):
    return f"https://raw.githubusercontent.com/{owner}/{name}"


def touch():
    open(".init.stamp", "w").close()


def lose(msg, e=None):
    print(msg)
    print("You will need to do the initialization steps manually.")
    print("Read scripts/first-run.py for more instructions how to do this.")
    if e:
        print(
            "\nHere's an additional error message which may help diagnose the problem."
        )
        raise e
    sys.exit(1)


try:
    my_repo_url = git.remote("get-url", "origin")
except Exception as e:
    lose("Could not use git to find my own repository URL", e)

https_url = re.match(r"https://github.com/(.*)/(.*)/?", str(my_repo_url))
ssh_url = re.match(r"git@github.com:(.*)/(.*)/?", str(my_repo_url))
if not any([https_url, ssh_url]):
    lose(
        f"My git repository URL ({my_repo_url}) didn't look what I expected - are you hosting this on github?"
    )

owner, reponame = m[1], m[2]

if owner == BASE_OWNER and reponame == BASE_REPONAME:
    print("I am being run on the upstream repository (probably due to CI)")
    print("All I'm going to do is create the touch file and quit.")
    touch()
    sys.exit()

# INITIALIZATION STEPS

# First, the README file contains URLs to pages in the `gh-pages` branch of the
# repo. When initially cloned, these URLs will point to the
# googlefonts/Unified-Font-Repository itself. But downstream users want links
# and badges about their own font, not ours! So any URLs need to be adjusted to
# refer to the end user's repository.

readme = open("README.md").read()

print(
    "Fixing URLs:", web_url(BASE_OWNER, BASE_REPONAME), "->", web_url(owner, reponame)
)
readme = readme.replace(web_url(BASE_OWNER, BASE_REPONAME), web_url(owner, reponame))
# In the badges, the URLs to raw.githubusercontent.com are URL-encoded as they
# are passed to shields.io.
print(
    "Fixing URLs:",
    quote(raw_url(BASE_OWNER, BASE_REPONAME), safe=""),
    "->",
    quote(raw_url(owner, reponame), safe=""),
)
readme = readme.replace(
    quote(raw_url(BASE_OWNER, BASE_REPONAME), safe=""),
    quote(raw_url(owner, reponame), safe=""),
)

with open("README.md", "w") as fh:
    fh.write(readme)

# Finally, we add a "touch file" called ".init.stamp" to the repository which
# prevents this first-run process from being run again.
touch()
