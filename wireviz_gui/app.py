import logging
from io import StringIO
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import showerror, showinfo

from graphviz import ExecutableNotFound
from PIL import ImageTk
from tk_tools import ToolTip
from wireviz.wireviz import Harness, parse
from wireviz.DataClasses import Connector, Cable, Metadata, Options, Tweak
from yaml import YAMLError

from wireviz_gui._base import BaseFrame, ToplevelBase
from wireviz_gui.dialogs import AboutFrame, AddCableFrame, AddConnectionFrame, AddConnectorFrame
from wireviz_gui.mating_dialog import AddMateDialog
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

        self._menu = Menu(self,
                          open_file=self._io_frame.open_file,
                          save=self._io_frame.save_file,
                          save_as=self._io_frame.save_as_file,
                          export_all=self._io_frame.export_all,
                          refresh=self._io_frame.parse_text,
                          reload_file=self._io_frame.reload_file,
                          about=self._about)
        self.config(menu=self._menu)

        self.bind_all('<Control-o>', lambda _: self._io_frame.open_file())
        self.bind_all('<Control-s>', lambda _: self._io_frame.save_file())
        self.bind_all('<Control-r>', lambda _: self._io_frame.reload_file())

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

        self._current_file_path = None
        self._harness = Harness(Metadata(), Options(), Tweak())

        r = 0
        self._button_frame = ButtonFrame(self,
                                         on_click_add_connector=self.add_connector,
                                         on_click_add_cable=self.add_cable,
                                         on_click_add_connection=self.add_connection,
                                         on_click_add_mate=self.add_mate,
                                         on_click_export=self.export_all,
                                         on_click_refresh=self.parse_text)
        # todo: re-enable when buttons and dialogs are working better
        self._button_frame.grid(row=r, column=0, sticky='ew')

        r += 1
        self._structure_view_frame = StructureViewFrame(self,
                                                        on_update_callback=self.refresh_view,
                                                        harness=self._harness)
        # todo: re-enable when structure view is working better
        # self._structure_view_frame.grid(row=r, column=0, sticky='ew')

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

    def add_mate(self):
        import yaml
        top = ToplevelBase(self)
        top.title('Mate Connectors')

        def on_save(yaml_snippet):
            current_text = self._text_entry_frame.get()
            try:
                data = yaml.safe_load(current_text) or {}
                if 'connections' not in data:
                    data['connections'] = []

                new_connection = yaml.safe_load(yaml_snippet)
                data['connections'].append(new_connection[0])

                # Clear the text entry and insert the updated YAML
                self._text_entry_frame.clear()
                self._text_entry_frame.append(yaml.dump(data, default_flow_style=False, sort_keys=False))

            except yaml.YAMLError as e:
                showerror('YAML Error', f'Error processing existing YAML: {e}')
                return

            top.destroy()
            self.parse_text()

        AddMateDialog(top, harness=self._harness, on_save_callback=on_save)\
            .grid()

    def open_file(self):
        file_name = askopenfilename(
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        if not file_name:
            return

        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            self._text_entry_frame.clear()
            self._text_entry_frame.append(content)
            self._current_file_path = file_name
            self.parse_text()
        except Exception as e:
            showerror('Open Error', f'Could not open file:\n{e}')

    def reload_file(self):
        if self._current_file_path:
            try:
                with open(self._current_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._text_entry_frame.clear()
                self._text_entry_frame.append(content)
                self.parse_text()
            except Exception as e:
                showerror('Reload Error', f'Could not reload file:\n{e}')
        else:
            showinfo('Reload Info', 'No file to reload.')

    def save_file(self):
        if self._current_file_path:
            yaml_input = self._text_entry_frame.get()
            if yaml_input.strip() == '':
                return

            # Validate YAML before saving
            try:
                parse(inp=yaml_input, return_types=('harness',))
            except YAMLError as e:
                showerror('Save Error', f'Invalid YAML content:\n{e}')
                return
            except Exception as e:
                showerror('Save Error', f'Invalid Wireviz YAML:\n{e}')
                return

            try:
                with open(self._current_file_path, 'w', encoding='utf-8') as f:
                    f.write(yaml_input)
            except Exception as e:
                showerror('Save Error', f'Could not save file:\n{e}')
        else:
            self.save_as_file()

    def save_as_file(self):
        yaml_input = self._text_entry_frame.get()
        if yaml_input.strip() == '':
            return

        # Validate YAML before saving
        try:
            parse(inp=yaml_input, return_types=('harness',))
        except YAMLError as e:
            showerror('Save Error', f'Invalid YAML content:\n{e}')
            return
        except Exception as e:
            showerror('Save Error', f'Invalid Wireviz YAML:\n{e}')
            return

        file_name = asksaveasfilename(
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        if file_name is None or file_name.strip() == '':
            return

        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(yaml_input)
            self._current_file_path = file_name
        except Exception as e:
            showerror('Save Error', f'Could not save file:\n{e}')

    def save_yaml(self):
        """Deprecated: use save_file or save_as_file"""
        self.save_file()

    def export_all(self):
        file_name = asksaveasfilename()
        if file_name is None or file_name.strip() == '':
            return

        path = Path(file_name)
        yaml_input = self._text_entry_frame.get()

        if yaml_input.strip() != '':
            try:
                parse(
                    inp=yaml_input,
                    output_dir=path.parent,
                    output_name=path.stem,
                    output_formats=('png', 'svg', 'html'),
                )
            except (ExecutableNotFound, FileNotFoundError):
                showerror('Error', 'Graphviz executable not found; Make sure that the '
                                   'executable is installed and in your system PATH')
                return
            except Exception as e:
                showerror('Error', f'An unexpected error occurred:\n{e}')
                return

    def parse_text(self):
        """
        This is where the data is read from the text entry and parsed into an image
        :return:
        """
        yaml_input = self._text_entry_frame.get()
        if yaml_input.strip() != '':
            try:
                png_data, new_harness = parse(
                    inp=yaml_input,
                    return_types=('png', 'harness')
                )
                self._harness.connectors = new_harness.connectors
                self._harness.cables = new_harness.cables
                self._harness.connections = new_harness.connections
                self._harness.mates = new_harness.mates
                self._harness.additional_bom_items = new_harness.additional_bom_items

                self.refresh_view(png_data)
            except YAMLError as e:
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
            except (ExecutableNotFound, FileNotFoundError):
                showerror('Error', 'Graphviz executable not found; Make sure that the '
                                   'executable is installed and in your system PATH')
                return
            except Exception as e:
                showerror('Error', f'An unexpected error occurred:\n{e}')
                return

        self._text_entry_frame.highlight_line(None)

    def refresh_view(self, png_data=None):
        if png_data:
            try:
                photo = ImageTk.PhotoImage(data=png_data)
                self._harness_view_frame.update_image(photo_image=photo)
            except Exception as e:
                showerror('Graph Creation Error', f'There was an error parsing the last request: {e}')
                return

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
            self._logger.debug('There appears to be no data in the '
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
                 on_click_add_mate: callable,
                 on_click_export: callable,
                 on_click_refresh: callable,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        c = 0
        self._add_conn_img = tk.PhotoImage(data=add_box_fill)
        add_conn_btn = tk.Button(self, image=self._add_conn_img, command=on_click_add_connector)
        add_conn_btn.grid(row=0, column=c, sticky='ew')
        ToolTip(add_conn_btn, 'Add Connector')

        c += 1
        self._add_cable_img = tk.PhotoImage(data=add_circle_fill)
        add_cable_btn = tk.Button(self, image=self._add_cable_img, command=on_click_add_cable)
        add_cable_btn.grid(row=0, column=c, sticky='ew')
        ToolTip(add_cable_btn, 'Add Cable')

        c += 1
        self._add_connect_img = tk.PhotoImage(data=links_fill)
        add_connection_btn = tk.Button(self, image=self._add_connect_img, command=on_click_add_connection)
        add_connection_btn.grid(row=0, column=c, sticky='ew')
        ToolTip(add_connection_btn, 'Add Connection')

        c += 1
        self._add_mate_img = tk.PhotoImage(data=links_fill)
        add_mate_btn = tk.Button(self, image=self._add_mate_img, command=on_click_add_mate)
        add_mate_btn.grid(row=0, column=c, sticky='ew')
        ToolTip(add_mate_btn, 'Mate Connectors')

        c += 1
        self._export_img = tk.PhotoImage(data=folder_transfer_fill)
        export_img_btn = tk.Button(self, image=self._export_img, command=on_click_export)
        export_img_btn.grid(row=0, column=c, sticky='ew')
        ToolTip(export_img_btn, 'Export Image')

        c += 1
        self._refresh_img = tk.PhotoImage(data=refresh_fill)
        refresh_img_btn = tk.Button(self, image=self._refresh_img, command=on_click_refresh, **self._heading)
        refresh_img_btn.grid(row=0, column=c, sticky='ew')
        ToolTip(refresh_img_btn, 'Refresh Image')


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

    def append(self, text: str):
        self._text.insert('end', text)

    def clear(self):
        self._text.delete('1.0', 'end')

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
