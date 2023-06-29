#!/usr/bin/env python3
"""
Script to generate LaTeX beamer overlay slides from an SVG file containing
multiple layers.  Based on Beamerscape by jboren, translted from perl to python
with a little hlep from chatgp.

Usage: svg_to_beamer_overlay.py FILENAME

Arguments: FILENAME The name of the input SVG file.

Example: svg_to_beamer_overlay.py foo.svg

This will create the directory `foo` which contains one pdf-file per layer and
the latex file overlay.tex.  Include in your latexfile as
\input{./foo/overlay.tex}

Note, you need to call this script from the directory that contains your latex
file.  You may have to modify \textblockorigin{0mm}{10mm} in your latex file.
"""

import argparse
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate LaTeX beamer overlay slides from an SVG file containing multiple layers."
    )
    parser.add_argument(
        "filename", metavar="FILENAME", help="the name of the input SVG file"
    )
    args = parser.parse_args()

    # Resolve input file path
    # this will use the fqfn
    # svgfile = Path(args.filename).resolve()
    # this will use the filename relative to the input directory
    svgfile = Path(args.filename)

    # Robust get file layers
    parser = ET.XMLParser()
    tree = ET.parse(str(svgfile), parser=parser)
    root = tree.getroot()
    layers = root.findall(".//{http://www.w3.org/2000/svg}g")

    # Generate and touch the overlay path
    overlay_path = Path(f"./{svgfile.parent}/{svgfile.stem}")
    # create dir and test if ok
    overlay_path.mkdir(parents=True, exist_ok=True)
    # create empty file
    (overlay_path / "overlay.tex").touch()

    print(overlay_path)

    # Open the tex file
    tex_path = overlay_path / "overlay.tex"
    with tex_path.open("w") as texfile:
        # Export the layers
        texfile.write("%overlays!")
        for layer in layers:
            # Get layer info
            id = layer.get("id")
            label = layer.get("{http://www.inkscape.org/namespaces/inkscape}label")
            if label:
                # Parse overlay spec
                overlay_spec = "+-"

                # Get file layers
                if "<" in label and ">" in label:
                    overlay_spec = label.split("<", 1)[1].split(">", 1)[0]

                # Debug/info spew
                print(f"layer id='{id}' label='{label}' overlay_spec='{overlay_spec}'")

                outfile = overlay_path / id
                subprocess.run(
                    [
                        "inkscape",
                        str(svgfile),
                        "--export-dpi=200",
                        "-C",
                        "-i",
                        id,
                        "-j",
                        f"--export-filename={outfile}.pdf",
                    ]
                )

                # Create tex for this layer
                texfile.write(
                    f"""
  %% Layer "{label}"
  \\pgfdeclareimage[height=0.9\\textheight]{{{id}}}{{{outfile}}}
  \\begin{{textblock}}{{1}}(0.1,0)
    \\pgfuseimage<{overlay_spec}>{{{id}}}
  \\end{{textblock}}\n"""
                )


if __name__ == "__main__":
    main()
