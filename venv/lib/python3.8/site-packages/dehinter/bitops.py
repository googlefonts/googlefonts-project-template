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


def is_bit_k_set(int_val: int, k: int) -> bool:
    """Tests if the value of bit at offset k in an integer is set"""
    return (int_val & (1 << k)) != 0


def clear_bit_k(int_val: int, k: int) -> int:
    """Clears the bit at offset k"""
    return int_val & ~(1 << k)


def set_bit_k(int_val: int, k: int) -> int:
    """Sets the bit at offset k"""
    return int_val | (1 << k)
