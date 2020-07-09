# Purpose

To provide an easy-to-use graphical interface for [wireviz](https://github.com/formatc1702/WireViz).

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

# Manual Installation

Those familiar with python and virtual environments will be able
to knock this out pretty quickly.  Those not familiar... will have to wait for
a release.  I anticipate that I will release some sort of nice package on the heels 
of the first [wireviz](https://github.com/formatc1702/WireViz) release.  The pull
requested that enabled the GUI to provide previews has already been accepted, but not
merged into the `main` branch so I expect an initial release in the coming weeks.

## Manual Installation of... Everything

Where there are `git clones`, I'm assuming that we are working from the `C:\code\`
directory.  Adjust as you see fit.

## Clone this Repository

    C:\code\>git clone https://github.com/slightlynybbled/wireviz-gui
    C:\code\>cd wireviz-gui
    C:\code\wireviz-gui\>

## Create and Activate your Virtual Environment

    C:\code\wireviz-gui\>virtualenv -p python3 venv
    C:\code\wireviz-gui\>venv\Scripts\activate.bat
    (venv) C:\code\wireviz-gui\>

## Install `wireviz`

This is *not* pip-installable so we have to download and install manually for 
the time being:

    (venv) C:\code\wireviz-gui\>cd ..
    (venv) C:\code\>git clone https://github.com/formatc1702/WireViz
    (venv) C:\code\>cd WireViz
    (venv) C:\code\WireViz\>python setup.py install
    
!!! NOTE !!! As of this writing, the [pull request](https://github.com/formatc1702/WireViz/pull/55) 
enabling this features has not been merged to the `main` branch!  You will have 
to checkout the `dev` branch for this to work!
    
## Execution

To run the gui:

    (venv) C:\code\WireViz>cd ..\wireviz-gui
    (venv) C:\code\>python -m wireviz_gui
