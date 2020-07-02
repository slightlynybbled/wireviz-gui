import logging
from tkinter import Frame, Menu


class BaseFrame(Frame):
    _normal = {'font': ('Arial', 12)}
    _heading = {'font': ('Arial', 16)}

    def __init__(self, parent, loglevel, **kwargs):
        self._parent = parent
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        super().__init__(self._parent, **kwargs)


class BaseMenu(Menu):
    def __init__(self, parent, loglevel=logging.INFO, **kwargs):
        self._parent = parent
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)
        super().__init__(self._parent, tearoff=False, **kwargs)
