# beamerscape
convert inkscape layers to latex beamer slides

## About
This script takes an Inkscape .svg as input, and generates pdf files corresponding to each of the layers and a LaTeX file that uses the LaTeX Beamer commands to incrementally overlay them. It will export the layers into a directory with the same basename as the .svg file. The layers will be exported in pdf format to preserve transparency.

A python version of https://github.com/jbohren/beamerscape

## Installation

This script requires the following libraries:
 - argparse
 - subprocess
 - xml
 - pathlib
 
Most of these are installed by default (at least under linux). If in doubt install conda.

Download the script, and call it as `python beamerscape.py` or set it as executable and copy to `/usr/local/bin/`
