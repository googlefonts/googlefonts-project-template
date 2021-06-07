# Copyright 2019 Source Foundry Authors and Contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import Tuple, Union


def get_filesize(filepath: Union[str, bytes, "os.PathLike[str]"]) -> Tuple[str, str]:
    """Returns formatted file size tuple fit for printing to end user."""
    filesize = os.path.getsize(filepath)
    kb_factor = 1 << 10
    mb_factor = 1 << 20

    if filesize < kb_factor:
        size_string = "B"
        formatted_filesize = float(filesize)
    elif kb_factor <= filesize < mb_factor:
        size_string = "KB"
        formatted_filesize = filesize / float(kb_factor)
    else:
        size_string = "MB"
        formatted_filesize = filesize / float(mb_factor)

    return "{0:.2f}".format(formatted_filesize), size_string
