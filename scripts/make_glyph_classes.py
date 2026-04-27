"""
Generate the file src/features/classes.fea which contains
glyph classes that capture all alternates for each glyph.
"""

import ufoLib2

from pathlib import Path

src_dir = Path(Path(__file__).resolve().parent, "../src/").resolve()
font = ufoLib2.Font.open(
    (src_dir / "AnnotationMono_Regular.ufo").resolve(), lazy=True
)

file = (src_dir / "features" / "classes.fea").open("w")


file.writelines("\n# Suffixes\n")
for g in font.keys():
    all_alts = [
        n for n in font.keys()
        if n == g or n.startswith(g + ".")
    ]

    file.writelines(f"@{g} = [{" ".join(all_alts)}];\n")

file.writelines("\n# Italics\n")
file.writelines(f"@italicizable = [{" ".join([g for g in font.keys() if f"{g}.ital" in font])}];\n")
file.writelines(f"@italicized = [{" ".join([f"{g}.ital" for g in font.keys() if f"{g}.ital" in font])}];\n")

file.writelines("\n# Plain un-loopy forms for some italics\n")
file.writelines(f"@unloopable = [{" ".join([g for g in font.keys() if f"{g}.plain" in font])}];\n")
file.writelines(f"@unlooped = [{" ".join([f"{g}.plain" for g in font.keys() if f"{g}.plain" in font])}];\n")
file.writelines("\n")
file.writelines(f"@unloopable_f = [{" ".join([g for g in font.keys() if g.startswith("f") and f"{g}.plain" in font])}];\n")
file.writelines(f"@unlooped_f = [{" ".join([f"{g}.plain" for g in font.keys() if g.startswith("f") and f"{g}.plain" in font])}];\n")
file.writelines("\n")
file.writelines(f"@unloopable_g = [{" ".join([g for g in font.keys() if g.startswith("g") and f"{g}.plain" in font])}];\n")
file.writelines(f"@unlooped_g = [{" ".join([f"{g}.plain" for g in font.keys() if g.startswith("g") and f"{g}.plain" in font])}];\n")
file.writelines("\n")
file.writelines(f"@unloopable_j = [{" ".join([g for g in font.keys() if g.startswith("j") and f"{g}.plain" in font])}];\n")
file.writelines(f"@unlooped_j = [{" ".join([f"{g}.plain" for g in font.keys() if g.startswith("j") and f"{g}.plain" in font])}];\n")
file.writelines("\n")
file.writelines(f"@unloopable_l = [{" ".join([g for g in font.keys() if g.startswith("l") and f"{g}.plain" in font])}];\n")
file.writelines(f"@unlooped_l = [{" ".join([f"{g}.plain" for g in font.keys() if g.startswith("l") and f"{g}.plain" in font])}];\n")
file.writelines("\n")
file.writelines(f"@unloopable_y = [{" ".join([g for g in font.keys() if g.startswith("y") and f"{g}.plain" in font])}];\n")
file.writelines(f"@unlooped_y = [{" ".join([f"{g}.plain" for g in font.keys() if g.startswith("y") and f"{g}.plain" in font])}];\n")

file.close()
