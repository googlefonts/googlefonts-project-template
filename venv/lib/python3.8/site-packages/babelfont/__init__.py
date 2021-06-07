import os
import sys
import pkgutil
import warnings


class addUnderscoreProperty:
    def __init__(self, prop):
        self.prop = prop

    def __call__(self, original_class):
        setattr(original_class, "_get_" + self.prop, lambda x: getattr(x, "_" + self.prop, None))
        setattr(original_class, "_set_" + self.prop, lambda x, v: setattr(x, "_" + self.prop, v))
        return original_class


class Babelfont:
    convertors = []

    @classmethod
    def _load_convertors(cls):
        if cls.convertors:
            return
        convertorpath = os.path.join(
            os.path.dirname(sys.modules[cls.__module__].__file__), "convertors"
        )
        # Additional plugin path here?
        loaders = pkgutil.iter_modules([convertorpath])
        for loader, module_name, is_pkg in loaders:
            if is_pkg:
                continue
            _module = loader.find_module(module_name).load_module(module_name)
            cls.convertors.append(_module)

    @classmethod
    def open(cls, filename, **kwargs):
        warnings.warn("Call to deprecated function open, use load instead.",
                      category=DeprecationWarning)
        return cls.load(filename, **kwargs)

    @classmethod
    def load(cls, filename, **kwargs):
        cls._load_convertors()
        for c in cls.convertors:
            if c.can_load(filename):
                return c.load(filename, **kwargs)
        raise NotImplementedError

    @classmethod
    def save(cls, obj, filename):
        cls._load_convertors()
        for c in cls.convertors:
            if c.can_save(filename):
                return c.save(obj, filename)
        raise NotImplementedError
