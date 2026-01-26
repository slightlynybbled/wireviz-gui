import unittest
from unittest.mock import MagicMock, patch
import sys

# Patch importlib.metadata.version
patch_version = patch("importlib.metadata.version", return_value="0.0.0+test")
patch_version.start()


class FakeMenu:
    def __init__(self, parent=None, tearoff=0, **kwargs):
        self.calls = []
        self.children_menus = []

    def add_command(self, **kwargs):
        self.calls.append(("add_command", kwargs))

    def add_cascade(self, **kwargs):
        self.calls.append(("add_cascade", kwargs))
        if "menu" in kwargs:
            self.children_menus.append(kwargs["menu"])

    def add_separator(self, **kwargs):
        self.calls.append(("add_separator", kwargs))


class FakeTkModule:
    Menu = FakeMenu
    Frame = MagicMock()
    PhotoImage = MagicMock()
    Toplevel = MagicMock()
    Button = MagicMock()
    Label = MagicMock()
    # Add other things used by _base or menus if needed


class TestMenuStructure(unittest.TestCase):
    def setUp(self):
        # Clean up modules
        for module in list(sys.modules.keys()):
            if module.startswith("wireviz_gui"):
                del sys.modules[module]
        if "tkinter" in sys.modules:
            del sys.modules["tkinter"]

    def test_file_menu_structure(self):
        with patch.dict(sys.modules, {"tkinter": FakeTkModule}):
            from wireviz_gui.menus import FileMenu

            parent = MagicMock()
            callbacks = {
                "open_file": MagicMock(),
                "save": MagicMock(),
                "save_as": MagicMock(),
                "save_graph_image": MagicMock(),
                "export_all": MagicMock(),
                "refresh": MagicMock(),
                "reload_file": MagicMock(),
                "new_file": MagicMock(),
                "examples": {"ex1": "content"},
                "load_example": MagicMock(),
            }

            menu = FileMenu(parent, **callbacks)

            # menu is instance of FileMenu(BaseMenu(FakeMenu))
            # so it has .calls populated

            labels = [
                kwargs.get("label")
                for method, kwargs in menu.calls
                if method == "add_command"
            ]

            self.assertIn("New (CTRL+N)", labels)
            self.assertIn("Open (CTRL+O)", labels)
            self.assertIn("Save (CTRL+S)", labels)
            self.assertIn("Save As...", labels)

            self.assertNotIn("Save Graph Image", labels)
            self.assertNotIn("Export All", labels)

            # Check Submenus
            cascade_labels = [
                kwargs.get("label")
                for method, kwargs in menu.calls
                if method == "add_cascade"
            ]
            self.assertIn("Export", cascade_labels)

            # Find Export Menu
            # It should be passed in add_cascade
            export_menu = None
            for method, kwargs in menu.calls:
                if method == "add_cascade" and kwargs.get("label") == "Export":
                    export_menu = kwargs.get("menu")
                    break

            self.assertIsNotNone(export_menu)

            # Check Export Menu Items
            export_labels = [
                kwargs.get("label")
                for method, kwargs in export_menu.calls
                if method == "add_command"
            ]
            self.assertIn("Graph Image (PNG)...", export_labels)
            self.assertIn("All Formats (PNG, SVG, HTML)...", export_labels)

    def test_menu_passes_new_file(self):
        with patch.dict(sys.modules, {"tkinter": FakeTkModule}):
            from wireviz_gui.menus import Menu, FileMenu
            # For this test, we want to intercept FileMenu creation inside Menu.
            # But changing FileMenu inside the module after import is hard.
            # However, we can inspect the created menu if we can access it.

            # Menu creates self.file_menu (or passes it to add_cascade)
            # We can check the menu passed to add_cascade("File", ...)

            parent = MagicMock()
            callbacks = {
                "open_file": MagicMock(),
                "save": MagicMock(),
                "save_as": MagicMock(),
                "save_graph_image": MagicMock(),
                "export_all": MagicMock(),
                "refresh": MagicMock(),
                "reload_file": MagicMock(),
                "about": MagicMock(),
                "new_file": MagicMock(),
                "load_example": MagicMock(),
                "close_tab": MagicMock(),
            }

            main_menu = Menu(parent, **callbacks)

            # Find File menu
            file_menu = None
            for method, kwargs in main_menu.calls:
                if method == "add_cascade" and kwargs.get("label") == "File":
                    file_menu = kwargs.get("menu")
                    break

            self.assertIsNotNone(file_menu)
            # Check if "New" command exists in file_menu
            labels = [
                kwargs.get("label")
                for method, kwargs in file_menu.calls
                if method == "add_command"
            ]
            self.assertIn("New (CTRL+N)", labels)


if __name__ == "__main__":
    unittest.main()
