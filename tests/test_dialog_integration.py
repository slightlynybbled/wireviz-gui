import unittest
from unittest.mock import MagicMock, patch

import yaml
from wireviz.DataClasses import Metadata, Options, Tweak
from wireviz.wireviz import Harness

from wireviz_gui.app import Application, InputOutputFrame
from wireviz_gui.dialogs import AddCableFrame, AddConnectionFrame, AddConnectorFrame
from wireviz_gui.mating_dialog import AddMateDialog


class TestDialogIntegration(unittest.TestCase):
    @patch("wireviz_gui.app.tk.Tk")
    @patch("wireviz_gui.app.tk.PhotoImage")
    @patch("wireviz_gui.app.ttk.Notebook")
    def test_add_connector_integration(self, mock_notebook, mock_photo, mock_tk):
        # Setup the app/frame logic manually without full GUI
        # We want to test InputOutputFrame._update_yaml_section

        # Create a mock InputOutputFrame (without calling __init__ fully if possible, or mocking grid)
        with (
            patch("wireviz_gui.app.InputOutputFrame.grid"),
            patch("wireviz_gui.app.ButtonFrame"),
            patch("wireviz_gui.app.StructureViewFrame"),
            patch("wireviz_gui.app.TextEntryFrame") as MockTextEntry,
            patch("wireviz_gui.app.HarnessViewFrame"),
        ):
            # Instantiate
            parent = MagicMock()
            frame = InputOutputFrame(parent)

            # Setup text entry mock
            text_entry_instance = MockTextEntry.return_value
            text_entry_instance.get.return_value = "connectors: {}"  # Initial YAML

            # Test Adding Connector
            new_connector_data = {"X1": {"type": "D-Sub", "pincount": 9}}

            # Call the update method directly
            frame._update_yaml_section("connectors", new_connector_data)

            # Verify text entry was cleared and appended with new YAML
            text_entry_instance.clear.assert_called()
            args, _ = text_entry_instance.append.call_args
            generated_yaml = args[0]

            parsed = yaml.safe_load(generated_yaml)
            self.assertIn("connectors", parsed)
            self.assertIn("X1", parsed["connectors"])
            self.assertEqual(parsed["connectors"]["X1"]["type"], "D-Sub")

    def test_dialog_outputs(self):
        # Verify dialogs produce the expected dict structure
        harness = MagicMock()
        harness.connectors = {}
        harness.cables = {}

        # --- Connector ---
        cb = MagicMock()
        # Ensure Entry returns distinct mocks
        with (
            patch("wireviz_gui.dialogs.tk.Label"),
            patch(
                "wireviz_gui.dialogs.tk.Entry",
                side_effect=lambda *args, **kwargs: MagicMock(),
            ) as MockEntry,
            patch("wireviz_gui.dialogs.tk.Button"),
            patch("wireviz_gui.dialogs.tk.Frame"),
            patch("wireviz_gui.dialogs.tk.BooleanVar"),
            patch("wireviz_gui.dialogs.tk.StringVar"),
        ):
            dialog = AddConnectorFrame(MagicMock(), harness, on_save_callback=cb)
            # Now we can configure the distinct mocks attached to self
            dialog._name_entry.get.return_value = "X2"
            dialog._type_entry.get.return_value = "Molex"
            dialog._manuf_entry.get.return_value = ""
            dialog._mpn_entry.get.return_value = ""
            dialog._ipm_entry.get.return_value = ""
            dialog._subtype_entry.get.return_value = ""

            dialog._pins_frame = MagicMock()
            dialog._pins_frame.pin_numbers = [1, 2]
            dialog._pins_frame.pinout = ["GND", "VCC"]

            dialog._save()

            cb.assert_called_once()
            data = cb.call_args[0][0]
            self.assertIn("X2", data)
            self.assertEqual(data["X2"]["type"], "Molex")
            self.assertEqual(data["X2"]["pincount"], 2)

        # --- Cable ---
        cb.reset_mock()
        with (
            patch("wireviz_gui.dialogs.tk.Label"),
            patch(
                "wireviz_gui.dialogs.tk.Entry",
                side_effect=lambda *args, **kwargs: MagicMock(),
            ),
            patch("wireviz_gui.dialogs.tk.Button"),
            patch("wireviz_gui.dialogs.tk.Frame"),
            patch(
                "wireviz_gui.dialogs.ttk.Combobox",
                side_effect=lambda *args, **kwargs: MagicMock(),
            ) as MockCombo,
            patch("wireviz_gui.dialogs.ttk.Checkbutton"),
            patch("wireviz_gui.dialogs.tk.BooleanVar"),
            patch("wireviz_gui.dialogs.tk.StringVar"),
        ):
            dialog = AddCableFrame(MagicMock(), harness, on_save_callback=cb)
            dialog._name_entry.get.return_value = "W1"
            dialog._manuf_entry.get.return_value = ""
            dialog._mpn_entry.get.return_value = ""
            dialog._ipm_entry.get.return_value = ""
            dialog._type_entry.get.return_value = ""
            dialog._length_entry.get.return_value = ""

            dialog._gauge_cb.get.return_value = "0.25"
            dialog._gauge_unit_cb.get.return_value = "mm2"

            dialog._wires_frame = MagicMock()
            dialog._wires_frame.colors = ["WH", "BK"]
            dialog._wires_frame.wire_numbers = [1, 2]

            dialog._save()

            cb.assert_called_once()
            data = cb.call_args[0][0]
            self.assertIn("W1", data)
            self.assertEqual(data["W1"]["gauge"], 0.25)
            self.assertEqual(data["W1"]["gauge_unit"], "mm2")
            self.assertEqual(data["W1"]["colors"], ["WH", "BK"])

        # --- Connection ---
        cb.reset_mock()
        with (
            patch("wireviz_gui.dialogs.tk.Label"),
            patch("wireviz_gui.dialogs.tk.Button"),
            patch(
                "wireviz_gui.dialogs.ttk.Combobox",
                side_effect=lambda *args, **kwargs: MagicMock(),
            ),
        ):
            dialog = AddConnectionFrame(MagicMock(), harness, on_save_callback=cb)

            dialog._from_connector_cb.get.return_value = "X1"
            dialog._through_cable_cb.get.return_value = "W1"
            dialog._to_connector_cb.get.return_value = "X2"
            dialog._from_conn_pin_cb.get.return_value = "1"
            dialog._through_cable_pin.get.return_value = "1"
            dialog._to_conn_pin_cb.get.return_value = "1"

            dialog._save()

            cb.assert_called_once()
            data = cb.call_args[0][0]
            expected = [{"X1": 1}, {"W1": 1}, {"X2": 1}]
            self.assertEqual(data, expected)


if __name__ == "__main__":
    unittest.main()
