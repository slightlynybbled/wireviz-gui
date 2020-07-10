import logging
import tkinter as tk
from tkinter.messagebox import showerror
import tkinter.ttk as ttk
import webbrowser

from wireviz.DataClasses import Connector

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
    def __init__(self, parent,
                 on_save_callback: callable = None,
                 loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

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
        tk.Label(self, text='Category:', **self._normal)\
            .grid(row=r, column=0, sticky='e')
        self._cat_entry = tk.Entry(self)
        self._cat_entry.grid(row=r, column=1, sticky='ew')

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

    def _save(self):
        name = self._name_entry.get().strip()
        manuf = self._manuf_entry.get().strip()
        mpn = self._mpn_entry.get().strip()
        ipm = self._ipm_entry.get().strip()
        category = self._cat_entry.get().strip()
        type = self._type_entry.get().strip()
        subtype = self._subtype_entry.get().strip()

        kwargs = {}
        if name:
            kwargs['name'] = name
        if category:
            kwargs['manufacturer'] = manuf
        if category:
            kwargs['manufacturer_part_number'] = mpn
        if category:
            kwargs['internal_part_number'] = ipm
        if category:
            kwargs['category'] = category
        if type:
            kwargs['type'] = type
        if subtype:
            kwargs['subtype'] = subtype
        kwargs['pinout'] = self._pins_frame.pinout

        try:
            connector = Connector(**kwargs)
        except Exception as e:
            showerror('Invalid Input', f'{e}')
            return

        if self._on_save_callback is not None:
            self._on_save_callback(connector)


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
