import logging
import tkinter as tk
import webbrowser

from wireviz_gui._base import BaseFrame
from wireviz_gui.images import logo


class AboutFrame(BaseFrame):
    def __init__(self, parent, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._logo_img = tk.PhotoImage(data=logo)

        r = 0
        tk.Label(self, image=self._logo_img)\
            .grid(row=r, column=0, columnspan=2)

        r += 1
        tk.Label(self, text='by jason r. jones', **self._normal)\
            .grid(row=r, column=0, columnspan=2)

        r += 1
        ttk.Separator(self, orient='horizontal').grid(row=r, column=0, columnspan=2, sticky='ew')

        r += 1
        tk.Label(self, text='built on ', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        wireviz_label = tk.Label(self, text='WireViz', **self._link)
        wireviz_label.grid(row=r, column=1, sticky='w')
        wireviz_label.bind('<Button-1>', lambda _: webbrowser.open('https://github.com/formatc1702/WireViz'))

        r += 1
        tk.Label(self, text='built on ', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        graphviz_label = tk.Label(self, text='graphviz', **self._link)
        graphviz_label.grid(row=r, column=1, sticky='w')
        graphviz_label.bind('<Button-1>', lambda _: webbrowser.open('https://graphviz.org/'))

        r += 1
        tk.Label(self, text='icons provided by ', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        remix_label = tk.Label(self, text='REMIX ICON', **self._link)
        remix_label.grid(row=r, column=1, sticky='w')
        remix_label.bind('<Button-1>', lambda _: webbrowser.open('https://remixicon.com/'))


class AddConnectorFrame(BaseFrame):
    def __init__(self, parent, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)