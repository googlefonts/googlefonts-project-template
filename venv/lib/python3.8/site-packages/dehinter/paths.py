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
from typing import Union


def filepath_exists(filepath: Union[bytes, str, "os.PathLike[str]"]) -> bool:
    """Tests a file path string to confirm that the file exists on the file system"""
    return os.path.isfile(filepath)


def get_default_out_path(
    filepath: os.PathLike,
) -> Union[str, bytes]:
    """Returns an updated file path that is used as dehinted file default when user
    does not specify an out file path."""
    dir_path, file_path = os.path.split(filepath)
    file_name, file_extension = os.path.splitext(file_path)
    default_file_name = file_name + "-dehinted" + file_extension
    return os.path.join(dir_path, default_file_name)
