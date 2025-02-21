"""
Remove glyphs in non-Regular UFOs which match the Regular one exactly.
"""

import ufoLib2

from pathlib import Path

src_dir = Path(Path(__file__).resolve().parent, "../src/").resolve()
regular = ufoLib2.Font.open((src_dir / "AnnotationMono_Regular.ufo").resolve(), lazy=True)
for ufo in src_dir.glob("*.ufo"):
    if ufo.name.endswith("_Regular.ufo"):
        continue

    font = ufoLib2.Font.open(ufo.resolve(), lazy=True)

    remove = []
    for g in font:
        if g.name is None or g.name not in regular:
            continue
        r = regular[g.name]
        if g == r:
            print(f"Removing {g.name} from {ufo}")
            remove.append(g.name)

    for n in remove:
        del font[n]

    font.save()
