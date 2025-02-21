"""
Rename all glyphs to their nice names from glyphsLib
"""

import ufoLib2
from glyphsLib.glyphdata import GlyphData
from importlib.resources import files

from pathlib import Path


def getGlyphData() -> GlyphData:
    path = files("glyphsLib.data") / "GlyphData.xml"
    with path.open("rb") as f:
        return GlyphData.from_files(f)


gd = getGlyphData()
u2n = {int(k, 16): v["name"].replace('-', '.') for k, v in gd.unicodes.items()}

src_dir = Path(Path(__file__).resolve().parent, "../src/").resolve()
for ufo in src_dir.glob("*.ufo"):
    font = ufoLib2.Font.open(ufo.resolve(), lazy=True)

    rename = []
    for g in font:
        if g.unicode in u2n and g.name != u2n[g.unicode]:
            rename.append((g.name, u2n[g.unicode]))

    for n, nn in rename:
        if nn in font and font[n] == font[nn]:
            print(f"Font already has {nn}, and it's identical to {n}, deleting {n}")
            del font[n]
            continue

        print(f"Renaming {n} to {nn}")
        font.renameGlyph(n, nn)

    font.save()
