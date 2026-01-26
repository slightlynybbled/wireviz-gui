import unittest
from unittest.mock import MagicMock, patch

# Import the classes we want to test.
# Note: We need to patch dependencies before importing if they do side-effects at import time,
# but here imports are safe. However, instantiation requires tk.
from wireviz_gui.app import HarnessViewFrame, InputOutputFrame


class TestImageExport(unittest.TestCase):
    @patch("wireviz_gui._base.Frame")  # Patch Frame in _base where BaseFrame is defined
    @patch("wireviz_gui.app.tk.Canvas")
    @patch("wireviz_gui.app.tk.Scrollbar")
    def test_harness_view_frame_save_image(self, mock_scroll, mock_canvas, mock_frame):
        # Setup
        parent = MagicMock()
        frame = HarnessViewFrame(parent)

        # Test 1: No image
        frame._image = None
        frame.save_image("test.png")
        # Should not raise exception and logging error

        # Test 2: With image
        mock_image = MagicMock()
        frame._image = mock_image
        frame.save_image("test.png")
        mock_image.save.assert_called_with("test.png")

    @patch("wireviz_gui.app.tk.Tk")
    @patch("wireviz_gui.app.tk.PhotoImage")
    @patch("wireviz_gui.app.ttk.Notebook")
    def test_input_output_frame_save_graph_image(
        self, mock_notebook, mock_photo, mock_tk
    ):
        # Mocking dependencies of InputOutputFrame
        # We also need to patch BaseFrame's init or Frame to avoid GUI calls
        with (
            patch("wireviz_gui._base.Frame"),
            patch("wireviz_gui.app.InputOutputFrame.grid"),
            patch("wireviz_gui.app.ButtonFrame"),
            patch("wireviz_gui.app.StructureViewFrame"),
            patch("wireviz_gui.app.TextEntryFrame"),
            patch("wireviz_gui.app.HarnessViewFrame") as MockHarnessViewFrame,
            patch("wireviz_gui.app.asksaveasfilename") as mock_asksave,
            patch("wireviz_gui.app.ttk.PanedWindow"),
        ):
            parent = MagicMock()
            frame = InputOutputFrame(parent)
            harness_view_mock = MockHarnessViewFrame.return_value

            # Case 1: No image in harness view
            harness_view_mock.has_image.return_value = False
            with patch("wireviz_gui.app.showinfo") as mock_showinfo:
                frame.save_graph_image()
                mock_showinfo.assert_called_with("Save Image", "No image to save.")
                mock_asksave.assert_not_called()

            # Case 2: Image exists, user cancels save
            harness_view_mock.has_image.return_value = True
            mock_asksave.return_value = ""
            frame.save_graph_image()
            harness_view_mock.save_image.assert_not_called()

            # Case 3: Image exists, user selects file
            mock_asksave.return_value = "path/to/save.png"
            frame.save_graph_image()
            harness_view_mock.save_image.assert_called_with("path/to/save.png")


if __name__ == "__main__":
    unittest.main()
