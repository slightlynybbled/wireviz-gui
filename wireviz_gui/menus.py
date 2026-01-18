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
                 load_example: callable = None,
                 close_tab: callable = None,
                 examples: dict = None,
                 loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        self.add_cascade(label='File', menu=FileMenu(self._parent,
                                                     open_file=open_file,
                                                     save=save,
                                                     save_as=save_as,
                                                     export_all=export_all,
                                                     refresh=refresh,
                                                     reload_file=reload_file,
                                                     load_example=load_example,
                                                     close_tab=close_tab,
                                                     examples=examples))
        self.add_cascade(label='Help', menu=HelpMenu(self._parent, about=about))


class FileMenu(BaseMenu):
    def __init__(self, parent,
                 open_file: callable,
                 save: callable,
                 save_as: callable,
                 export_all: callable,
                 refresh: callable,
                 reload_file: callable,
                 load_example: callable = None,
                 close_tab: callable = None,
                 examples: dict = None,
                 loglevel=logging.INFO, **kwargs):
        super().__init__(parent=parent, loglevel=loglevel, **kwargs)

        self.add_command(label='Open (CTRL+O)', command=lambda: open_file())
        self.add_command(label='Save (CTRL+S)', command=lambda: save())
        self.add_command(label='Save As', command=lambda: save_as())
        self.add_command(label='Export All', command=lambda: export_all())

        if examples and load_example:
            examples_menu = tk.Menu(self, tearoff=0)
            for name, content in examples.items():
                examples_menu.add_command(label=name, command=lambda c=content, n=name: load_example(n, c))
            self.add_cascade(label='Examples', menu=examples_menu)

        self.add_command(label='Refresh Image (CTRL+L)', command=lambda: refresh())
        self.add_command(label='Reload File (CTRL+R)', command=lambda: reload_file())

        if close_tab:
            self.add_separator()
            self.add_command(label='Close Tab (CTRL+W)', command=lambda: close_tab())


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
