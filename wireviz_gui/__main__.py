import logging
import os
from pathlib import Path

import click

from wireviz_gui.app import Application


@click.command()
@click.option(
    "--graphviz-path",
    "-p",
    default=None,
    help="The path on which GraphViz binary may be found.",
)
def main(graphviz_path):
    if graphviz_path is not None:
        _graphviz_path = Path(__file__).parent / ".." / "graphviz_238_win32" / "bin"

        if os.environ["PATH"].endswith(os.pathsep):
            os.environ["PATH"] += str(_graphviz_path)
        else:
            os.environ["PATH"] += os.pathsep + str(_graphviz_path)

    logging.basicConfig(level=logging.DEBUG)
    Application()


main()
