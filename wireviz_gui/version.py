import importlib.metadata

try:
    __version__ = importlib.metadata.version("wireviz_gui")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.3.0+dev"
