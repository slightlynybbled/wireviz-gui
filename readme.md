# Purpose

To provide an easy-to-use graphical interface for [wireviz](https://github.com/wireviz/WireViz).

# Screenshot

As this was just started, it is pretty basic, but there is lots of potential.

![screenshot](/docs/screenshots/screenshot.png)

# Motivation

As you can see, the graphics generated using wireviz are quite good with minimum
effort... for those familiar with the command line.  I work with many people who
would love the output files, but hate the interface and, thus, would not use it.

# Pre-Requisites

## Install `graphviz`

Head over to the [graphviz download page](https://graphviz.org/download/) and install
a version of graphviz that suits your system.  Most of the guys I'm targetting will
use some version of Windows, so I'm doing most of my development there.

I use the `winget` method.

Be sure that you add the `graphviz` directory to your `PATH` (look in 
environment variables)!!!  I had to perform a restart after this step.

# Executable

There is an executable available!  I built the executable based on the current-day 
`dev` branch of [wireviz](https://github.com/formatc1702/WireViz), but it works
well enough.  Go to the [releases](https://github.com/slightlynybbled/wireviz-gui/releases/tag/v0.1.0),
download the `wireviz-gui_vX.X.X_YYY.exe` and execute.  This makes for a nice "try/see"
environment.

# Unit Testing

    $>uv run pytest

# Installation

This assumes you are familiar with Python, virtual environments, and `pip`.

1. **Clone this repository:**
   ```bash
   git clone https://github.com/slightlynybbled/wireviz-gui
   cd wireviz-gui
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python -m wireviz_gui
   ```
