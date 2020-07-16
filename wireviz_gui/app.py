import logging
from io import StringIO
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror

from graphviz import ExecutableNotFound
from PIL import ImageTk
from wireviz.DataClasses import Cable, Connector
from wireviz.Harness import Harness
from wireviz.wireviz import parse
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from wireviz_gui._base import BaseFrame, ToplevelBase
from wireviz_gui.dialogs import AboutFrame, AddCableFrame, AddConnectionFrame, AddConnectorFrame
from wireviz_gui.images import *
from wireviz_gui.menus import Menu


class Application(tk.Tk):
    def __init__(self, loglevel=logging.INFO, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        super().__init__(**kwargs)

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
                          refresh=self._io_frame.parse_text, about=self._about)
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

        self._harness = Harness()

        r = 0
        self._button_frame = ButtonFrame(self,
                                         on_click_add_connector=self.add_connector,
                                         on_click_add_cable=self.add_cable,
                                         on_click_add_connection=self.add_connection,
                                         on_click_export=self.export_all,
                                         on_click_refresh=self.parse_text)
        self._button_frame.grid(row=r, column=0, sticky='ew')

        r += 1
        self._structure_view_frame = StructureViewFrame(self,
                                                        on_update_callback=self.refresh_view,
                                                        harness=self._harness)
        self._structure_view_frame.grid(row=r, column=0, sticky='ew')

        r += 1
        self._text_entry_frame = TextEntryFrame(self,
                                                on_update_callback=self.parse_text)
        self._text_entry_frame.grid(row=r, column=0, sticky='ew')

        r += 1
        self._harness_view_frame = HarnessViewFrame(self)
        self._harness_view_frame.grid(row=r, column=0, sticky='ew')

    def add_connector(self):
        top = ToplevelBase(self)
        top.title('Add Connector')

        def on_save():
            top.destroy()
            self.refresh_view()

        AddConnectorFrame(top, harness=self._harness, on_save_callback=on_save)\
            .grid()

    def add_cable(self):
        top = ToplevelBase(self)
        top.title('Add Cable')

        def on_save():
            top.destroy()
            self.refresh_view()

        AddCableFrame(top, harness=self._harness, on_save_callback=on_save)\
            .grid()

    def add_connection(self):
        top = ToplevelBase(self)
        top.title('Add Connection')

        def on_save():
            top.destroy()
            self.refresh_view()

        AddConnectionFrame(top, harness=self._harness, on_save_callback=on_save)\
            .grid()

    def export_all(self):
        self.refresh_view()

        file_name = asksaveasfilename()
        if file_name is None or file_name.strip() == '':
            return

        path = Path(file_name)

        if self._text_entry_frame.get().strip() != '':
            try:
                parse(
                    yaml_input=self._text_entry_frame.get(),
                    file_out=path
                )
            except ExecutableNotFound:
                showerror('Error', 'Graphviz executable not found; Make sure that the '
                                   'executable is installed and in your system PATH')
                return
            return

        self._harness.output(
            filename=path,
            fmt=('png', 'svg'),
            view=False
        )

    def parse_text(self):
        """
        This is where the data is read from the text entry and parsed into an image

        :return:
        """
        if self._text_entry_frame.get().strip() != '':
            f_in = StringIO(self._text_entry_frame.get())

            try:
                harness = parse(f_in, return_types='harness')
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

            # copy the attributes of the new harness
            self._harness.connectors = harness.connectors
            self._harness.cables = harness.cables
            self._additional_bom_items = harness.additional_bom_items

        self._text_entry_frame.highlight_line(None)

        self.refresh_view()

    def refresh_view(self):
        try:
            photo = ImageTk.PhotoImage(data=self._harness.png)
        except KeyError:
            showerror('Graph Creation Error', 'There was an error parsing the last request')
            return

        self._harness_view_frame\
            .update_image(photo_image=photo)

        self._structure_view_frame.refresh()


class StructureViewFrame(BaseFrame):
    def __init__(self, parent, harness: Harness,
                 on_update_callback: callable = None, loglevel=logging.INFO):
        super().__init__(parent=parent, loglevel=loglevel)

        self._harness = harness
        self._on_update_callback = on_update_callback

        self.refresh(False)

    def _load_connector_dialog(self, connector: Connector):
        top = ToplevelBase(self)
        top.title('Add Connector')

        def on_save():
            top.destroy()
            self.refresh(True)

        AddConnectorFrame(top,
                          harness=self._harness,
                          connector_name=str(connector),
                          on_save_callback=on_save).grid()

    def refresh(self, execute_callback: bool = False):
        for child in self.winfo_children():
            child.destroy()

        tk.Label(self, text='Harness Elements:', **self._normal)\
            .grid(row=0, column=0, sticky='ew')

        if self._harness.connectors == {} and self._harness.cables == {}:
            # a nag screen; todo: replace when wireviz is updated so
            # that parse will return an instance of `Harness`
            self._logger.warning('There appears to be no data in the '
                                 '`Harness` instance; Perhaps the '
                                 'instance is blank?')
            tk.Label(self, text='(none)', **self._normal) \
                .grid(row=0, column=1, sticky='ew')

        c = 1
        for connector in self._harness.connectors:
            conn_label = tk.Label(self, text=f'{connector}', **self._link)
            conn_label.grid(row=0, column=c, sticky='ew')
            conn_label.bind('<Button-1>',
                            lambda _, cl=connector: self._load_connector_dialog(cl))
            c += 1

        for cable in self._harness.cables:
            cable_label = tk.Label(self, text=f'{cable}', **self._link)
            cable_label.grid(row=0, column=c, sticky='ew')
            cable_label.bind('<Button-1>', lambda _, cb=cable: print(cb))
            c += 1

        if execute_callback and self._on_update_callback is not None:
            self._on_update_callback()


class ButtonFrame(BaseFrame):
    def __init__(self, parent,
                 on_click_add_connector: callable,
                 on_click_add_cable: callable,
                 on_click_add_connection: callable,
                 on_click_export: callable,
                 on_click_refresh: callable,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        c = 0
        self._add_conn_img = tk.PhotoImage(data=add_box_fill)
        tk.Button(self, image=self._add_conn_img, command=on_click_add_connector)\
            .grid(row=0, column=c, sticky='ew')

        c += 1
        self._add_cable_img = tk.PhotoImage(data=add_circle_fill)
        tk.Button(self, image=self._add_cable_img, command=on_click_add_cable)\
            .grid(row=0, column=c, sticky='ew')

        c += 1
        self._add_connect_img = tk.PhotoImage(data=links_fill)
        tk.Button(self, image=self._add_connect_img, command=on_click_add_connection)\
            .grid(row=0, column=c, sticky='ew')

        c += 1
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


class HarnessViewFrame(BaseFrame):
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Application()
