# coding: utf8
from rstr import xeger
import string
import re
import random
from sre_yield import AllStrings


class StringBrewer(object):
    """Generate random strings matching a pattern.

Patterns are specified in the StringBrewer pattern language, and are made
up of two parts: a *recipe* and a set of *ingredients*. A recipe is
essentially a modified form of regular expression; whitespace is not
significant, and each ingredient name is replaced by its definition. An
*ingredient* is a space-separated list of items; each item is either a
character (specified either as a literal character or as a Unicode
codepoint in hexadecimal), a range of characters separated by hyphens,
or a union of items separated by commas. Ingredients may also contain
references to other ingredients.

This is best understood by example. The pattern below generates
Telugu morphemes::

    # Generate random Telugu-like morphemes
    (Base HalantGroup{0,2} TopPositionedVowel?){1,3}

    Base = క-న,ప-హ
    Halant = 0C4D
    HalantGroup = Halant Base
    TopPositionedVowel = 0C46-0C48,0C4A-0C4C

The first line is a comment; the second is the recipe, and the blank line
denotes the beginning of the ingredients list. Let's look at the ingredients.
A ``Base`` is any character either in the range ``0x0C15-0C28`` or ``0C2A-0C39``.
(We specified these as literals, just because we could). A ``Halant`` is the
character ``0x0C4D``. A ``HalantGroup`` is a halant followed by a base.

Now you understand the ingredients, the recipe is simple to understand if you
think in terms of regular expression syntax: a base followed by zero, one or
two halant groups, plus an optional top-positioned vowel, all repeated between
one and three times.
"""

    def __init__(self, from_string=None, from_file=None, recipe=None, ingredients=None):
        """Initializes a StringBrewer object

        You must provide *either* a file name, a string, or a recipe
        string and ingredients dictionary.

        Args:
            from_file: A file name of a file containing a pattern.
            from_string: A pattern in a string.
            recipe: The recipe part of a pattern.
            ingredients: A dictionary of regular expressions.
        """

        if from_file:
            self.parse_recipe_file(from_file)
        elif from_string:
            self.parse_recipe_string(from_string)
        elif recipe and ingredients:
            self.recipe = recipe
            self.ingredients = ingredients
        else:
            raise ValueError(
                "Need to instantiate StringBrewer with file, string or recipe"
            )
        self._initialize()

    def _initialize(self):
        if len(self.ingredients.keys()) > 52:
            raise ValueError("Too many ingredients")
        self.regex = self.recipe_to_regex(self.recipe)

    def parse_recipe_file(self, filename):
        with open(filename, "r") as file:
            self.parse_recipe_string(file.read())

    def recipe_to_regex(self, recipe):
        regex = recipe
        for k, v in self.ingredients.items():
            v2 = v.replace("\\", "\\\\")
            regex = re.sub(f"\\b{k}\\b", "(?:" + v2 + ")", regex)
        regex = re.sub("\\s", "", regex)
        return regex

    def generate_all(self):
        """Generates a list of all combinations.

        If there are more than 100,000 combinations, an exception
        is raised to avoid running out of memory.
        """
        m = AllStrings(self.regex)
        if m.__len__() > 100_000:
            raise ValueError("Too many combinations to iterate all")
        return list(m)

    def generate(self, min_length=0, max_length=None):
        """Generates a single random combination.

        Args:
            min_length: Minimum length (zero if not specified)
            max_length: Maximum length (no maximum if not specified)
        """
        attempts = 0
        while attempts < 100:
            trial = xeger(self.regex)
            attempts = attempts + 1
            if max_length and len(trial) > max_length:
                continue
            if min_length and len(trial) < min_length:
                continue
            break
        return trial

    def parse_recipe_string(self, s):
        got_recipe = False
        self.ingredients = {}
        while len(s):
            s, sn = re.subn(r"^(\s+|#.*)", "", s)
            if sn:
                continue
            if not got_recipe:
                m = re.match(r"^(.*?)\s*$", s, flags=re.MULTILINE)
                if not m:
                    raise ValueError("Couldn't find recipe")
                self.recipe = m[1]
                got_recipe = True
                s = s[m.end() :]
                continue
            m = re.match(r"^(\w+)\s*=\s*(.*)\s*$", s, flags=re.MULTILINE)
            if not m:
                raise ValueError("Couldn't parse ingredients")
            s = s[m.end() :]
            self.ingredients[m[1]] = self.parse_ingredient(m[2])

    def parse_ingredient(self, ingredient):
        bits = re.split(r"\s+", ingredient)
        res = []
        for bit in bits:
            res.extend(self.parse_bit(bit))
        res = "".join(res)
        return res

    def parse_bit(self, bit):
        res = []
        if bit in self.ingredients:
            res.append(self.ingredients[bit])
        elif "," in bit:
            subbits = re.split(",", bit)
            # One of the elements
            res.append("(?:")
            res.append("|".join([self.parse_bit(b) for b in subbits]))
            res.append(")")
        elif "-" in bit:
            range_begin, range_end = re.split("-", bit)
            if len(range_begin) > 1:
                range_begin = int(range_begin, 16)
            else:
                range_begin = ord(range_begin)
            if len(range_end) > 1:
                range_end = int(range_end, 16)
            else:
                range_end = ord(range_end)
            res.append("[")
            res.append("\\u%04x" % range_begin)
            res.append("-")
            res.append("\\u%04x" % range_end)
            res.append("]")
        else:
            if len(bit) > 1:
                res.append("\\u%04x" % int(bit, 16))
            else:
                res.append("\\u%04x" % ord(bit))
        return "(?:" + ("".join(res)) + ")"


if __name__ == "__main__":
    s = StringBrewer(
        from_string="""

# Generate random Telugu-like morphemes
(Base HalantGroup{0,2} TopPositionedVowel?){1,3}

Base = 0C15-0C28,0C2A-0C39
Halant = 0C4D
HalantGroup = Halant Base
TopPositionedVowel = 0C46-0C48,0C4A-0C4C

    """
    )
    try:
        fail()
        print(s.generate_all())
    except Exception as e:
        print(s.regex)
        for i in range(1, 10):
            print(s.generate())
