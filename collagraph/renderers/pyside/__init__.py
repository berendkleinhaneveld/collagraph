from functools import lru_cache


def camel_case(event, split, upper=False):
    prefix, *parts = event.split(split)
    return "".join(
        [prefix.capitalize() if upper else prefix]
        + [part.capitalize() for part in parts]
    )


@lru_cache(maxsize=None)
def attr_name_to_method_name(name, setter=False):
    sep = "-"
    if "_" in name:
        sep = "_"

    prefix = f"set{sep}" if setter else ""
    return camel_case(f"{prefix}{name}", sep)


@lru_cache(maxsize=None)
def _ci_lookup(cls, method_name):
    """Case-insensitive lookup of method_name on cls, returns the actual name."""
    lower = method_name.lower()
    for attr in dir(cls):
        if attr.lower() == lower:
            return attr
    return None


def resolve_method_name(obj, method_name):
    """Resolve a method name on obj, falling back to case-insensitive lookup.

    Qt is not always consistent in its casing (e.g. ``setTristate`` vs the
    expected ``setTriState``).  When the exact name is not found on the
    object we try a case-insensitive match against the class hierarchy.
    """
    if hasattr(obj, method_name):
        return method_name
    return _ci_lookup(type(obj), method_name)


def call_method(method, args):
    """Method that allows for calling setters/methods with multiple arguments
    such as: `setColumnStretch` of `PySide6.QtWidgets.QGridLayout` which takes a
    column and stretch argument.
    """
    if isinstance(args, tuple):
        method(*args)
    else:
        method(args)
