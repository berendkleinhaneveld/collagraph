import logging

from PySide6.QtWidgets import QStackedWidget

from ...pyside_renderer import PySideRenderer
from .qobject import set_attribute as qobject_set_attribute

logger = logging.getLogger(__name__)


@PySideRenderer.register_insert(QStackedWidget)
def insert(self, el, anchor=None):
    el.setParent(self)
    if anchor:
        index = self.indexOf(anchor)
        self.insertWidget(index, el)
    else:
        self.addWidget(el)


@PySideRenderer.register_remove(QStackedWidget)
def remove(self, el):
    self.removeWidget(el)


@PySideRenderer.register_set_attr(QStackedWidget)
def set_attribute(self, attr, value):
    if attr == "size":
        self.resize(*value)
        return

    qobject_set_attribute(self, attr, value)
