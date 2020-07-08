import logging
from io import StringIO
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror
import webbrowser

from graphviz import ExecutableNotFound
from PIL import ImageTk
from wireviz.wireviz import parse
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from wireviz_gui._base import BaseFrame, ToplevelBase
from wireviz_gui.images import logo, refresh_fill, folder_transfer_fill, slightlynybbled_logo_small
from wireviz_gui.menus import Menu


class Application(tk.Tk):
    def __init__(self, loglevel=logging.INFO, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        super().__init__()

        self.title('wireviz-gui')

        self._icon = tk.PhotoImage(data=slightlynybbled_logo_small)
        self.tk.call('wm', 'iconphoto', self._w, self._icon)

        r = 0
        self._title_frame = TitleFrame(self)
        self._title_frame.grid(row=r, column=0, sticky='ew')

        r += 1
        self._io_frame = InputOutputFrame(self)
        self._io_frame.grid(row=r, column=0, sticky='ew')

        self._menu = Menu(self, export_all=self._io_frame.export_all,
                          refresh=self._io_frame.refresh, about=self._about)
        self.config(menu=self._menu)

        self.mainloop()

    def _about(self):
        top = ToplevelBase(self)
        top.title('About')
        AboutFrame(top).grid()


class TitleFrame(BaseFrame):
    def __init__(self, parent, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._logo_img = tk.PhotoImage(data=logo)

        r = 0
        tk.Label(self, image=self._logo_img)\
            .grid(row=r, column=0, sticky='news')


class InputOutputFrame(BaseFrame):
    def __init__(self, parent, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        r = 0
        self._button_frame = ButtonFrame(self,
                                         on_click_export=self.export_all,
                                         on_click_refresh=self.refresh)
        self._button_frame.grid(row=r, column=0, sticky='ew')

        r += 1
        self._text_entry_frame = TextEntryFrame(self,
                                                on_update_callback=self.refresh)
        self._text_entry_frame.grid(row=1, column=0, sticky='ew')

        r += 1
        self._harness_frame = HarnessFrame(self)
        self._harness_frame.grid(row=r, column=0, sticky='ew')

    def export_all(self):
        file_name = asksaveasfilename()
        if file_name is None or file_name.strip() == '':
            return

        try:
            parse(
                yaml_input=self._text_entry_frame.get(),
                file_out=file_name,
                generate_bom=True,
            )
        except ExecutableNotFound:
            showerror('Error', 'Graphviz executable not found; Make sure that the '
                               'executable is installed and in your system PATH')
            return

    def refresh(self):
        """
        This is where the data is read from the text entry and parsed into an image

        :return:
        """
        f_in = StringIO(self._text_entry_frame.get())

        try:
            data = parse(f_in, return_types=('png', ))[0]
        except (TypeError, ):
            showerror('Parse Error', 'Input is invalid or missing')
            return
        except (ParserError, ScannerError) as e:
            lines = str(e).lower()
            for line in lines.split('\n'):
                if 'line' in line:
                    # determine the line number that has a problem
                    parts = [l.strip() for l in line.split(',')]
                    part = [l for l in parts if 'line' in l][0]
                    error_line = part.split(' ')[1]
                    self._text_entry_frame.highlight_line(error_line)
                    break
            showerror('Parse Error', f'Input is invalid: {e}')
            return
        except ExecutableNotFound:
            showerror('Error', 'Graphviz executable not found; Make sure that the '
                               'executable is installed and in your system PATH')
            return

        photo = ImageTk.PhotoImage(data=data)

        self._harness_frame\
            .update_image(photo_image=photo)

        self._text_entry_frame.highlight_line(None)


class ButtonFrame(BaseFrame):
    def __init__(self, parent, on_click_export: callable, on_click_refresh: callable, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        c = 0
        self._export_img = tk.PhotoImage(data=folder_transfer_fill)
        tk.Button(self, image=self._export_img, command=on_click_export)\
            .grid(row=0, column=c, sticky='ew')

        c += 1
        self._refresh_img = tk.PhotoImage(data=refresh_fill)
        tk.Button(self, image=self._refresh_img, command=on_click_refresh, **self._heading)\
            .grid(row=0, column=c, sticky='ew')


class TextEntryFrame(BaseFrame):
    def __init__(self, parent, on_update_callback: callable = None, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._on_update_callback = on_update_callback

        self._text = tk.Text(self)
        self._text.grid(row=0, column=1, sticky='news')
        self._text.bind('<Control-l>', lambda _: self._updated())
        self._text.tag_config('highlight', background='yellow')

    def associate_callback(self, on_update_callback: callable):
        self._on_update_callback = on_update_callback

    def _updated(self):
        if self._on_update_callback is not None:
            self._on_update_callback()

    def get(self):
        return self._text.get('1.0', 'end')

    def highlight_line(self, line_number: str):
        self._text.tag_remove('highlight', f'0.0', 'end')

        if line_number is not None:
            self._text.tag_add('highlight', f'{line_number}.0', f'{line_number}.40')


class HarnessFrame(BaseFrame):
    def __init__(self, parent, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._label = tk.Label(self, text='(no harness defined)')
        self._label.grid(row=0, column=0, sticky='ew')
        self._pi = None  # photoimage data

    def update_image(self, photo_image: ImageTk.PhotoImage):
        self._pi = photo_image
        self._label.config(
            text=None,
            image=photo_image
        )


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Application()
