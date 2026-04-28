"""
Find composite glyphs that are missing variants corresponding
to variants of one ore more of the component glyphs.
"""

import ufoLib2
from pathlib import Path

src_dir = Path(Path(__file__).resolve().parent, "../src/").resolve()
font = ufoLib2.Font.open(
    (src_dir / "AnnotationMono_Regular.ufo").resolve(), lazy=True
)

VAR_COMP = "com.black-foundry.variable-components"

for glyph in font:
    component_names = []

    for cmp in glyph.components:
        component_names.append(cmp.baseGlyph)
    if VAR_COMP in glyph.lib:
        for cmp in glyph.lib[VAR_COMP]:
            component_names.append(cmp["base"])

    if len(component_names) == 0:
        continue

    for cmp in component_names:
        base_alternates = [
            g for g in font.keys()
            if g.startswith(cmp + ".")
        ]
        missing = []
        for alt in base_alternates:
            suffix = alt[len(cmp):]
            if glyph.name and glyph.name.endswith(suffix):
                continue
            alt_cmp = f"{glyph.name}{suffix}"
            if alt_cmp not in font:
                missing.append("/" + alt_cmp)

        if len(missing) > 0:
            print(f"/{glyph.name}  is missing {"  ".join(missing)}")
