import logging
import tkinter as tk

from wireviz_gui._base import BaseMenu


class Menu(BaseMenu):
    def __init__(self, parent,
                 save: callable,
                 export_all: callable,
                 refresh: callable,
                 about: callable,
                 loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        self.add_cascade(label='File', menu=FileMenu(self._parent, save=save, export_all=export_all, refresh=refresh))
        self.add_cascade(label='Help', menu=HelpMenu(self._parent, about=about))


class FileMenu(BaseMenu):
    def __init__(self, parent,
                 save: callable,
                 export_all: callable,
                 refresh: callable,
                 loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        command_lookup = {
            'Save (CTRL+S)': lambda: save(),
            'Export All':   lambda: export_all(),
            'Refresh (CTRL+L)':      lambda: refresh(),
        }

        for label, command in command_lookup.items():
            self.add_command(label=label, command=command)


class HelpMenu(BaseMenu):
    def __init__(self, parent, about: callable, loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        command_lookup = {
            'About': lambda: about()
        }

        for label, command in command_lookup.items():
            self.add_command(label=label, command=command)


if __name__ == '__main__':
    window = tk.Tk()

    menu = Menu(window)
    window.config(menu=menu)

    window.mainloop()
