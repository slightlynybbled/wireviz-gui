# Purpose

To provide an easy-to-use graphical interface for [wireviz](https://github.com/formatc1702/WireViz).

# Motivation

As you can see, the graphics generated using wireviz are quite good with minimum
effort... for those familiar with the command line.  I work with many people who
would love the output files, but hate the interface and, thus, would not use it.

Therefore, I'm going to give a good start to creating it!

# Installation

For the moment, this is not available as an executable or any other "nice" package,
so here it is.  Those familiar with python and virtual environments will be able
to knock this out pretty quickly.  Those not familiar... will have to wait for
a release.

Where there are `git clones`, I'm assuming that we are working from the `C:\code\`
directory.  Adjust as you see fit.

## Install `graphviz`

Head over to the [graphviz download page](https://graphviz.org/download/) and install
a version of graphviz that suits your system.  Most of the guys I'm targetting will
use some version of Windows, so I'm doing most of my development there.

I had the most success using the `winget` method.

Be sure that you add the `graphviz` directory to your `PATH` (look in 
environment variables)!!!  I had to perform a restart after this step.

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
    (venv) C:\code\>pip install .\WireViz
    
## Execution

To run the gui:

    (venv) C:\code\>cd wireviz-gui
    (venv) C:\code\>python -m wireviz_gui
