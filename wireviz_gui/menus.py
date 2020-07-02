import logging
import tkinter as tk

from wireviz_gui._base import BaseMenu


class Menu(BaseMenu):
    def __init__(self, parent, loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        self.add_cascade(label='File', menu=FileMenu(self._parent))
        self.add_cascade(label='Help', menu=HelpMenu(self._parent))


class FileMenu(BaseMenu):
    def __init__(self, parent, loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        command_lookup = {
            'Save':         lambda: print('clicked save'),
            'Export PNG':   lambda: print('exporting png...'),
            'Export All':   lambda: print('exporting all...'),
        }

        for label, command in command_lookup.items():
            self.add_command(label=label, command=command)


class HelpMenu(BaseMenu):
    def __init__(self, parent, loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        command_lookup = {
            'About':         lambda: print('clicked about')
        }

        for label, command in command_lookup.items():
            self.add_command(label=label, command=command)


if __name__ == '__main__':
    window = tk.Tk()

    menu = Menu(window)
    window.config(menu=menu)

    window.mainloop()
