import logging
import os
from pathlib import Path

from wireviz_gui.app import Application


_graphviz_path = Path(__file__).parent / '..' / 'graphviz_238_win32' / 'bin'

if os.environ['PATH'].endswith(os.pathsep):
    os.environ["PATH"] += str(_graphviz_path)
else:
    os.environ["PATH"] += os.pathsep + str(_graphviz_path)

logging.basicConfig(level=logging.DEBUG)
Application()
