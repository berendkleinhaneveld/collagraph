from PySide6.QtWidgets import QLCDNumber

from ... import PySideRenderer
from . import widget


@PySideRenderer.register_set_attr(QLCDNumber)
def set_attribute(self, attr, value):
    if attr == "value":
        self.display(value)
    else:
        widget.set_attribute(self, attr, value)
