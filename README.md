
# UPK Extractor

A small script written in Python that is designed to assist with the bulk extraction of sound files from certain Unreal Engine titles via the Unreal Package Extractor available at <https://www.gildor.org/downloads>.

Can easily be modified to target other extensions by anyone with a surface-level knowledge of Python (just update the `TARGET_EXTENSIONS` list).

Tested and working with game files from Batman: Arkham Asylum, amongst others.

## Usage

Download this repo from here, and the Unreal Package Extractor from Gildor's website (placing it in the same folder as upkbatch<area>.py).

Put all required <area>.upk files in the `INPUT` folder (this folder must be in the same folder as upkbatch<area>.py), and run upkbatch<area>.py. Extracted files will appear in `OUTPUT`.

## Requirements

- None, except Python. (Uses the `subprocess`, `pathlib`, `os`, `shutil` and `time` modules, which are all included in Python's standard library: <https://docs.python.org/3/library/index.html>.)



