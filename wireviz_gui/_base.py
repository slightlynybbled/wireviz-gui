import logging
from tkinter import Button, Frame, Label, Menu, PhotoImage, Toplevel

from wireviz_gui.images import slightlynybbled_logo_small

_norm_font = ("Arial", 12)
_heading_font = ("Arial", 16)

_link_fg = 'blue'
_alert_fg = 'red'


class BaseFrame(Frame):
    _normal = {"font": ("Arial", 12)}
    _link = {"font": ("Arial", 12), "fg": "blue"}
    _red = {"font": ("Arial", 12), "fg": "red"}
    _heading = {"font": ("Arial", 16)}

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


class ToplevelBase(Toplevel):
    def __init__(self, parent, loglevel=logging.INFO, **kwargs):
        self._parent = parent
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)
        super().__init__(self._parent, **kwargs)

        self._icon = PhotoImage(data=slightlynybbled_logo_small)
        self.tk.call("wm", "iconphoto", self._w, self._icon)


class NormButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(
            font=_norm_font,
            *args,
            **kwargs
        )


class HeadButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(
            font=_heading_font,
            *args,
            **kwargs
        )


class NormLabel(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(
            font=_norm_font,
            *args,
            **kwargs
        )


class AlertLabel(NormLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(
            fg=_alert_fg,
            *args,
            **kwargs
        )


class LinkLabel(NormLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(
            fg=_link_fg,
            *args,
            **kwargs
        )


class HeadLabel(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(
            font=_heading_font,
            *args,
            **kwargs
        )
