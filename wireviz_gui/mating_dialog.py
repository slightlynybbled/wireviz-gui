import logging
import tkinter as tk
from tkinter.messagebox import showerror
import tkinter.ttk as ttk
import webbrowser

from wireviz.wireviz import Harness

from wireviz_gui._base import BaseFrame


class AddMateDialog(BaseFrame):
    def __init__(
        self,
        parent,
        harness: Harness,
        on_save_callback: callable = None,
        loglevel=logging.INFO,
    ):
        super().__init__(parent, loglevel=loglevel)

        self._harness = harness
        self._on_save_callback = on_save_callback

        r = 0
        tk.Label(self, text="Mate Connectors", **self._heading).grid(
            row=r, column=0, columnspan=2, sticky="ew"
        )

        r += 1
        tk.Label(self, text="From:", **self._normal).grid(row=r, column=0, sticky="e")
        self._from_connector_cb = ttk.Combobox(
            self, values=list(self._harness.connectors.keys())
        )
        self._from_connector_cb.grid(row=r, column=1, sticky="ew")

        r += 1
        tk.Label(self, text="To:", **self._normal).grid(row=r, column=0, sticky="e")
        self._to_connector_cb = ttk.Combobox(
            self, values=list(self._harness.connectors.keys())
        )
        self._to_connector_cb.grid(row=r, column=1, sticky="ew")

        r += 1
        self._arrow_type_var = tk.StringVar(value="double")
        tk.Radiobutton(
            self,
            text="Whole Connector (==>)",
            variable=self._arrow_type_var,
            value="double",
            command=self._update_arrow_directions,
        ).grid(row=r, column=0, sticky="w")
        tk.Radiobutton(
            self,
            text="Pin-to-Pin (-->)",
            variable=self._arrow_type_var,
            value="single",
            command=self._update_arrow_directions,
        ).grid(row=r, column=1, sticky="w")

        r += 1
        self._arrow_direction_var = tk.StringVar(value="==>")
        self._arrow_direction_frame = tk.Frame(self)
        self._arrow_direction_frame.grid(row=r, column=0, columnspan=2, sticky="ew")
        self._update_arrow_directions()

        r += 1
        tk.Button(self, text="Save Mate", command=self._save, **self._normal).grid(
            row=r, column=0, columnspan=2, sticky="ew"
        )

    def _update_arrow_directions(self):
        for child in self._arrow_direction_frame.winfo_children():
            child.destroy()

        if self._arrow_type_var.get() == "double":
            directions = ["==>", "<==", "<==>", "=="]
        else:
            directions = ["-->", "<--", "<-->", "--"]

        self._arrow_direction_var.set(directions[0])

        for direction in directions:
            tk.Radiobutton(
                self._arrow_direction_frame,
                text=direction,
                variable=self._arrow_direction_var,
                value=direction,
            ).pack(side="left", expand=True)

    def _save(self):
        from_connector = self._from_connector_cb.get()
        to_connector = self._to_connector_cb.get()
        arrow = self._arrow_direction_var.get()

        if not from_connector or not to_connector:
            showerror("Error", 'Please select both "From" and "To" connectors.')
            return

        # Return a python list representing the connection: [from, arrow, to]
        # This will be appended to the 'connections' list in the harness data.
        mate_data = [from_connector, arrow, to_connector]

        if self._on_save_callback is not None:
            self._on_save_callback(mate_data)
