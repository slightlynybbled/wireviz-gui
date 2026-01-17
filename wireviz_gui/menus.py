import logging
import tkinter as tk

from wireviz_gui._base import BaseMenu


class Menu(BaseMenu):
    def __init__(self, parent,
                 open_file: callable,
                 save: callable,
                 save_as: callable,
                 export_all: callable,
                 refresh: callable,
                 reload_file: callable,
                 about: callable,
                 loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        self.add_cascade(label='File', menu=FileMenu(self._parent,
                                                     open_file=open_file,
                                                     save=save,
                                                     save_as=save_as,
                                                     export_all=export_all,
                                                     refresh=refresh,
                                                     reload_file=reload_file))
        self.add_cascade(label='Help', menu=HelpMenu(self._parent, about=about))


class FileMenu(BaseMenu):
    def __init__(self, parent,
                 open_file: callable,
                 save: callable,
                 save_as: callable,
                 export_all: callable,
                 refresh: callable,
                 reload_file: callable,
                 loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        command_lookup = {
            'Open (CTRL+O)': lambda: open_file(),
            'Save (CTRL+S)': lambda: save(),
            'Save As': lambda: save_as(),
            'Export All':   lambda: export_all(),
            'Refresh Image (CTRL+L)':      lambda: refresh(),
            'Reload File (CTRL+R)':        lambda: reload_file(),
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
