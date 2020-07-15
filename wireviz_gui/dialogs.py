import logging
import tkinter as tk
from tkinter.messagebox import showerror
import tkinter.ttk as ttk
import webbrowser

from wireviz.DataClasses import Connector, Cable, Connection
from wireviz.Harness import Harness
from wireviz.wv_colors import color_full
from wireviz.wv_helper import awg_equiv_table

from wireviz_gui._base import BaseFrame
from wireviz_gui.images import logo


def _name_is_duplicated(new_name, harness):
    names = list([c for c in harness.connectors.keys()])
    names += list([c for c in harness.cables.keys()])

    if new_name in names:
        showerror('Invalid Entry', '"Name" is duplicated')
        return True

    return False


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
    def __init__(self, parent,
                 harness: Harness,
                 connector_name: str = None,
                 on_save_callback: callable = None,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._harness = harness
        self._connector_name = connector_name
        self._on_save_callback = on_save_callback

        r = 0
        tk.Label(self, text='Add Connector', **self._heading)\
            .grid(row=r, column=0, columnspan=2, sticky='ew')

        r += 1
        tk.Label(self, text='Name:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._name_entry = tk.Entry(self)
        self._name_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Manufacturer:', **self._normal) \
            .grid(row=r, column=0, sticky='e')
        self._manuf_entry = tk.Entry(self)
        self._manuf_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Manuf. Part Number:', **self._normal) \
            .grid(row=r, column=0, sticky='e')
        self._mpn_entry = tk.Entry(self)
        self._mpn_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Internal Part Number:', **self._normal) \
            .grid(row=r, column=0, sticky='e')
        self._ipm_entry = tk.Entry(self)
        self._ipm_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Type:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._type_entry = tk.Entry(self)
        self._type_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Sub-Type:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._subtype_entry = tk.Entry(self)
        self._subtype_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        self._pins_frame = PinsFrame(self)
        self._pins_frame.grid(row=r, column=0, columnspan=2, sticky='ew')

        r += 1
        tk.Button(self, text='Add Pin',
                  command=lambda: self._pins_frame.add_pin(),
                  **self._normal)\
            .grid(row=r, column=0, columnspan=2, sticky='ew')

        r += 1
        tk.Button(self, text='Save Connector',
                  command=self._save,
                  **self._normal)\
            .grid(row=r, column=0, columnspan=2, sticky='ew')

        if self._connector_name is not None:
            r += 1
            tk.Button(self, text='Delete Connector',
                      command=self._delete,
                      **self._normal) \
                .grid(row=r, column=0, columnspan=2, sticky='ew')
            self._load()

    def _delete(self):
        self._harness.connectors.pop(self._connector_name)
        if self._on_save_callback is not None:
            self._on_save_callback()

    def _load(self):
        connector = self._harness.connectors[self._connector_name]
        self._name_entry.insert(0, f'{connector.name}')
        self._name_entry.config(state='disabled')

        if connector.manufacturer is not None:
            self._manuf_entry.insert(0, connector.manufacturer)
        if connector.manufacturer_part_number is not None:
            self._mpn_entry.insert(0, connector.manufacturer_part_number)
        if connector.internal_part_number is not None:
            self._ipm_entry.insert(0, connector.internal_part_number)
        if connector.type is not None:
            self._type_entry.insert(0, connector.type)
        if connector.subtype is not None:
            self._subtype_entry.insert(0, connector.subtype)

        # load PinsFrame
        self._pins_frame.load(connector.pinnumbers, connector.pinout)

    def _save(self):
        name = self._name_entry.get().strip()
        manuf = self._manuf_entry.get().strip()
        mpn = self._mpn_entry.get().strip()
        ipm = self._ipm_entry.get().strip()
        type = self._type_entry.get().strip()
        subtype = self._subtype_entry.get().strip()

        kwargs = {}
        if manuf:
            kwargs['manufacturer'] = manuf
        if mpn:
            kwargs['manufacturer_part_number'] = mpn
        if ipm:
            kwargs['internal_part_number'] = ipm
        if type:
            kwargs['type'] = type
        if subtype:
            kwargs['subtype'] = subtype

        self._pins_frame.update_all()
        kwargs['pinnumbers'] = self._pins_frame.pin_numbers
        kwargs['pinout'] = self._pins_frame.pinout
        kwargs['pincount'] = len(self._pins_frame.pin_numbers)

        try:
            self._harness.add_connector(name, **kwargs)
        except Exception as e:
            showerror('Invalid Input', f'{e}')
            return

        if self._on_save_callback is not None:
            self._on_save_callback()


class PinsFrame(BaseFrame):
    def __init__(self, parent,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._pin_frames = []

        self._redraw()

    def _redraw(self):
        for child in self.winfo_children():
            child.grid_forget()

        self._pin_frames = [pf for pf in self._pin_frames if pf.number is not None]

        if len(self._pin_frames) > 0:
            for i, frame in enumerate(self._pin_frames):
                frame.grid(row=i+1, column=0, sticky='ew')
            return

        tk.Label(self, text='(no pins)', **self._normal).grid(row=0, column=0, sticky='ew')

    @property
    def pin_numbers(self):
        pin_numbers = [p.number for p in self._pin_frames]

        return pin_numbers

    @property
    def pinout(self):
        return [p.name for p in self._pin_frames]

    def load(self, pinnumbers, pinout):
        for num, name in zip(pinnumbers, pinout):
            self._pin_frames.append(
                PinFrame(self, pin_number=num, pin_name=name, on_delete_callback=self._redraw)
            )
        self._redraw()

    def update_all(self):
        for pf in self._pin_frames:
            pf.refresh()

    def add_pin(self):
        if len(self._pin_frames) > 0:
            pin_nums = [f.number for f in self._pin_frames]
            next_num = max(pin_nums) + 1
        else:
            next_num = 1

        self._pin_frames.append(
            PinFrame(self, pin_number=next_num, on_delete_callback=self._redraw)
        )

        self._redraw()

    def _remove_pin(self, index):
        self._pin_frames.pop(index)
        self._redraw()


class PinFrame(BaseFrame):
    def __init__(self, parent,
                 pin_number: int,
                 pin_name: str = None,
                 on_delete_callback: callable = None,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._pin_number = pin_number
        self._pin_name = pin_name
        self._on_delete_callback = on_delete_callback

        self._pin_number_entry = tk.Entry(self)
        self._pin_number_entry.grid(row=0, column=0, sticky='ew')
        self._pin_number_entry.bind('<FocusOut>', lambda _: self._update_pin_number())
        self._pin_number_entry.bind('<Return>', lambda _: self._update_pin_number())

        self._pin_name_entry = tk.Entry(self)
        self._pin_name_entry.grid(row=0, column=1, sticky='ew')
        self._pin_name_entry.bind('<FocusOut>', lambda _: self._update_pin_name())
        self._pin_name_entry.bind('<Return>', lambda _: self._update_pin_name())
        self._pin_name_entry.insert(0, f'{self._pin_name}')

        self._x_label = tk.Label(self, text='X', **self._red)
        self._x_label.grid(row=0, column=2, sticky='ew')
        self._x_label.bind('<Button-1>', lambda _: self._delete())

        self._update_pin_number()
        self._update_pin_name()

    def refresh(self):
        self._update_pin_number()
        self._update_pin_name()

    def _update_pin_number(self):
        try:
            value = int(self._pin_number_entry.get())
        except ValueError:
            self._pin_number_entry.delete(0, 'end')
            self._pin_number_entry.insert(0, f'{self._pin_number}')
            return

        self._pin_number = value

    def _delete(self):
        self._pin_number = None

        if self._on_delete_callback is not None:
            self._on_delete_callback()

    def _update_pin_name(self):
        value = self._pin_name_entry.get().strip()
        if value == '':
            self._pin_number_entry.delete(0, 'end')
            self._pin_number_entry.insert(0, f'{self._pin_name}')
            return

        self._pin_name = value

    @property
    def number(self):
        return self._pin_number

    @property
    def name(self):
        return self._pin_name


class AddCableFrame(BaseFrame):
    def __init__(self, parent,
                 harness: Harness,
                 on_save_callback: callable = None,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._harness = harness
        self._on_save_callback = on_save_callback

        r = 0
        tk.Label(self, text='Add Cable', **self._heading)\
            .grid(row=r, column=0, columnspan=2, sticky='ew')

        r += 1
        tk.Label(self, text='Name:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._name_entry = tk.Entry(self)
        self._name_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Manufacturer:', **self._normal) \
            .grid(row=r, column=0, sticky='e')
        self._manuf_entry = tk.Entry(self)
        self._manuf_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Manuf. Part Number:', **self._normal) \
            .grid(row=r, column=0, sticky='e')
        self._mpn_entry = tk.Entry(self)
        self._mpn_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Internal Part Number:', **self._normal) \
            .grid(row=r, column=0, sticky='e')
        self._ipm_entry = tk.Entry(self)
        self._ipm_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Type:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._type_entry = tk.Entry(self)
        self._type_entry.grid(row=r, column=1, sticky='ew')

        r += 1
        tk.Label(self, text='Gauge Unit:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._gauge_unit_cb = ttk.Combobox(self, values=['AWG', 'mm\u00B2'])
        self._gauge_unit_cb.grid(row=r, column=1, sticky='ew')
        self._gauge_unit_cb.bind('<<ComboboxSelected>>', lambda _: self._update_gauge_list())

        r += 1
        tk.Label(self, text='Gauge:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._gauge_cb = ttk.Combobox(self)
        self._gauge_cb.grid(row=r, column=1, sticky='ew')
        tk.Label(self, text='AWG', **self._normal).grid(row=r, column=2, sticky='ew')

        r += 1
        tk.Label(self, text='Length:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._length_entry = tk.Entry(self)
        self._length_entry.grid(row=r, column=1, sticky='ew')
        tk.Label(self, text='mm', **self._normal).grid(row=r, column=2, sticky='ew')

        r += 1
        tk.Label(self, text='Shield:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._shield_var = tk.BooleanVar()
        self._shield_var.set(False)
        self._shield_cb = ttk.Checkbutton(self, variable=self._shield_var)
        self._shield_cb.grid(row=r, column=1, sticky='ew')

        r += 1
        self._wires_frame = WiresFrame(self)
        self._wires_frame.grid(row=r, column=0, columnspan=2, sticky='ew')

        r += 1
        tk.Button(self, text='Add Wire',
                  command=lambda: self._wires_frame.add_wire(),
                  **self._normal)\
            .grid(row=r, column=0, columnspan=2, sticky='ew')

        r += 1
        tk.Button(self, text='Save Cable',
                  command=self._save,
                  **self._normal)\
            .grid(row=r, column=0, columnspan=2, sticky='ew')

    def _update_gauge_list(self):
        gauge_unit = self._gauge_unit_cb.get().strip()

        if gauge_unit == 'mm\u00B2':
            gauge_list = [k for k, _ in awg_equiv_table.items()]
        else:
            gauge_list = [v for _, v in awg_equiv_table.items()]

        self._gauge_cb['values'] = gauge_list

    def _save(self):
        name = self._name_entry.get().strip()
        manuf = self._manuf_entry.get().strip()
        mpn = self._mpn_entry.get().strip()
        ipm = self._ipm_entry.get().strip()
        type = self._type_entry.get().strip()
        gauge = self._gauge_cb.get().strip()
        gauge_unit = self._gauge_unit_cb.get().strip()
        length = self._length_entry.get().strip()
        shield = self._shield_var.get()

        kwargs = {}
        if manuf:
            kwargs['manufacturer'] = manuf
        if mpn:
            kwargs['manufacturer_part_number'] = mpn
        if ipm:
            kwargs['internal_part_number'] = ipm
        if type:
            kwargs['type'] = type
        if gauge != '':
            try:
                kwargs['gauge'] = int(gauge)
            except ValueError:
                kwargs['gauge'] = float(gauge)
            except Exception:
                pass
        if gauge_unit:
            kwargs['gauge_unit'] = gauge_unit
        if length:
            try:
                kwargs['length'] = float(length)
            except ValueError as e:
                showerror('Invalid Input', e)
                return

        kwargs['shield'] = shield

        self._wires_frame.update_all()
        kwargs['colors'] = self._wires_frame.colors

        try:
            self._harness.add_cable(name, **kwargs)
        except Exception as e:
            showerror('Invalid Input', f'{e}')
            return

        if self._on_save_callback is not None:
            self._on_save_callback()


class WiresFrame(BaseFrame):
    def __init__(self, parent,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._wire_frames = []

        self._redraw()

    def _redraw(self):
        for child in self.winfo_children():
            child.grid_forget()

        self._wire_frames = [wf for wf in self._wire_frames if wf.number is not None]

        if len(self._wire_frames) > 0:
            for i, frame in enumerate(self._wire_frames):
                frame.grid(row=i+1, column=0, sticky='ew')
            return

        tk.Label(self, text='(no wires)', **self._normal).grid(row=0, column=0, sticky='ew')

    @property
    def wire_numbers(self):
        wire_numbers = [w.number for w in self._wire_frames]

        return wire_numbers

    @property
    def colors(self):
        return [p.color for p in self._wire_frames]

    def update_all(self):
        for pf in self._wire_frames:
            pf.parse_text()

    def add_wire(self):
        if len(self._wire_frames) > 0:
            pin_nums = [f.number for f in self._wire_frames]
            next_num = max(pin_nums) + 1
        else:
            next_num = 1

        self._wire_frames.append(
            WireFrame(self, wire_number=next_num, on_delete_callback=self._redraw)
        )

        self._redraw()

    def _remove_wire(self, index):
        self._wire_frames.pop(index)
        self._redraw()


class WireFrame(BaseFrame):
    def __init__(self, parent,
                 wire_number: int,
                 wire_color: str = None,
                 on_delete_callback: callable = None,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._wire_number = wire_number
        self._wire_color = wire_color
        self._on_delete_callback = on_delete_callback

        self._wire_number_entry = tk.Entry(self)
        self._wire_number_entry.grid(row=0, column=0, sticky='ew')
        self._wire_number_entry.bind('<FocusOut>', lambda _: self._update_wire_number())
        self._wire_number_entry.bind('<Return>', lambda _: self._update_wire_number())

        self._wire_color_cb = ttk.Combobox(self, values=list(color_full.keys()))
        self._wire_color_cb.grid(row=0, column=1, sticky='ew')
        self._wire_color_cb.insert(0, 'WH')
        self._wire_color_cb.bind('<FocusOut>', lambda _: self._update_wire_color())
        self._wire_color_cb.bind('<Return>', lambda _: self._update_wire_color())

        self._x_label = tk.Label(self, text='X', **self._red)
        self._x_label.grid(row=0, column=2, sticky='ew')
        self._x_label.bind('<Button-1>', lambda _: self._delete())

        self._update_wire_number()
        self._update_wire_color()

    def refresh(self):
        self._update_wire_number()
        self._update_wire_color()

    def _update_wire_number(self):
        try:
            value = int(self._wire_number_entry.get())
        except ValueError:
            self._wire_number_entry.delete(0, 'end')
            self._wire_number_entry.insert(0, f'{self._wire_number}')
            return

        self._wire_number = value

    def _delete(self):
        self._wire_number = None

        if self._on_delete_callback is not None:
            self._on_delete_callback()

    def _update_wire_color(self):
        value = self._wire_color_cb.get().strip()
        if value == '':
            self._wire_number_entry.delete(0, 'end')
            self._wire_number_entry.insert(0, f'{self._wire_color}')
            return

        self._wire_color = value

    @property
    def number(self):
        return self._wire_number

    @property
    def color(self):
        return self._wire_color


class AddConnectionFrame(BaseFrame):
    def __init__(self, parent,
                 harness: Harness,
                 on_save_callback: callable = None,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._harness = harness
        self._on_save_callback = on_save_callback

        r = 0
        tk.Label(self, text='Add Connection', **self._heading) \
            .grid(row=r, column=0, columnspan=3, sticky='ew')

        connectors = list(self._harness.connectors.keys())
        cables = list(self._harness.cables.keys())

        r += 1
        tk.Label(self, text='From', **self._normal)\
            .grid(row=r, column=0, sticky='ew')
        tk.Label(self, text='Through', **self._normal)\
            .grid(row=r, column=1, sticky='ew')
        tk.Label(self, text='To', **self._normal)\
            .grid(row=r, column=2, sticky='ew')

        r += 1
        self._from_connector_cb = ttk.Combobox(self, values=connectors)
        self._from_connector_cb.grid(row=r, column=0, sticky='ew')

        self._through_cable_cb = ttk.Combobox(self, values=cables)
        self._through_cable_cb.grid(row=r, column=1, sticky='ew')

        self._to_connector_cb = ttk.Combobox(self, values=connectors)
        self._to_connector_cb.grid(row=r, column=2, sticky='ew')

        r += 1
        self._from_conn_pin_cb = ttk.Combobox(self)
        self._from_conn_pin_cb.grid(row=r, column=0, sticky='ew')
        self._from_connector_cb.bind(
            '<<ComboboxSelected>>',
            lambda _, fcb=self._from_connector_cb, pcb=self._from_conn_pin_cb: self._update_conn_pins(fcb, pcb))

        self._through_cable_pin = ttk.Combobox(self)
        self._through_cable_pin.grid(row=r, column=1, sticky='ew')
        self._through_cable_cb.bind('<<ComboboxSelected>>', lambda _: self._update_through_cable_pins())

        self._to_conn_pin_cb = ttk.Combobox(self)
        self._to_conn_pin_cb.grid(row=r, column=2, sticky='ew')
        self._to_connector_cb.bind(
            '<<ComboboxSelected>>',
            lambda _, fcb=self._to_connector_cb, pcb=self._to_conn_pin_cb: self._update_conn_pins(fcb, pcb))

        r += 1
        tk.Button(self, text='Save Connection',
                  command=self._save,
                  **self._normal)\
            .grid(row=r, column=0, columnspan=3, sticky='ew')

    def _update_conn_pins(self, conn_cb, pin_cb):
        key = conn_cb.get()
        pins = self._harness.connectors[key].pinnumbers
        pin_cb['values'] = pins

    def _update_through_cable_pins(self):
        name = self._through_cable_cb.get()
        wire_numbers = [i+1 for i in range(self._harness.cables[name].wirecount)]
        self._through_cable_pin['values'] = wire_numbers

    def _save(self):
        data = {}
        data['from_name'] = self._from_connector_cb.get()
        data['via_name'] = self._through_cable_cb.get()
        data['to_name'] = self._to_connector_cb.get()

        try:
            data['from_pin'] = int(self._from_conn_pin_cb.get())
        except ValueError:
            data['from_pin'] = self._from_conn_pin_cb.get()

        try:
            data['via_pin'] = int(self._through_cable_pin.get())
        except ValueError:
            data['via_pin'] = self._through_cable_pin.get()

        try:
            data['to_pin'] = int(self._to_conn_pin_cb.get())
        except ValueError:
            data['to_pin'] = self._to_conn_pin_cb.get()

        # add connections
        self._harness.connect(**data)

        if self._on_save_callback is not None:
            self._on_save_callback()
