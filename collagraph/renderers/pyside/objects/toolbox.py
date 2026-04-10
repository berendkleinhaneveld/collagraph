import logging

from PySide6.QtWidgets import QToolBox

from ...pyside_renderer import PySideRenderer
from .qobject import set_attribute as qobject_set_attribute

logger = logging.getLogger(__name__)


@PySideRenderer.register_insert(QToolBox)
def insert(self, el, anchor=None):
    el.setParent(self)
    if anchor:
        index = self.indexOf(anchor)
        self.insertItem(index, el, el.title)
    else:
        self.addItem(el, el.title)


@PySideRenderer.register_remove(QToolBox)
def remove(self, el):
    index = self.indexOf(el)
    self.removeItem(index)


@PySideRenderer.register_set_attr(QToolBox)
def set_attribute(self, attr, value):
    if attr == "size":
        self.resize(*value)
        return

    qobject_set_attribute(self, attr, value)
