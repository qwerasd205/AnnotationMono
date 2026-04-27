"""
Prepare the build files, fixing them up before we call fontmake.

- Sets UPM
- Adds root fea
- Sets Panose
- Sets OS/2 fsSelection UseTypoMetrics
- Sets OS/2 winAscent and winDescent
"""

import ufoLib2
from pathlib import Path

def processFea(path):
    text = f"### START {path} ###\n"
    for l in Path(path).read_text().splitlines(True):
        if l.startswith("include("):
            text = text + processFea("./src/features/" + l[8:-3])
            text = text + f"### CONTINUE {path} ###\n"
        else:
            text = text + l
    text = text + f"\n### END {path} ###\n"
    return text

fea_text = processFea("./src/features/features.fea")

build_dir = Path(Path(__file__).resolve().parent, "./build/").resolve()
for ufo in build_dir.glob("*.ufo"):
    font = ufoLib2.Font.open(ufo.resolve(), lazy=True)
    font.info.unitsPerEm = 800
    font.features.text = fea_text
    font.info.openTypeOS2Panose = [3, 5, 0, 3, 4, 0, 2, 2, 11, 4]
    font.info.openTypeOS2WinAscent = 1150
    font.info.openTypeOS2WinDescent = 250
    font.info.openTypeOS2Selection = [7] # Use Typo Metrics (bit 7)
    font.save()
    if " Oblique" in ufo.name:
        ufo.rename(ufo.parent / ufo.name.replace(" Oblique", "[slnt=-15]"))
